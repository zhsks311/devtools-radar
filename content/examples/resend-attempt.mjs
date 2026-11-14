// One attempt, not an outbox implementation. Never call directly from a browser.
// Caller must atomically claim a durable outbox row BEFORE the first send and
// persist its immutable payload, key, firstAttemptAt and attempt outcomes.
// Use one event/version key, not Date.now(); retries must reuse the exact payload.
// Resend retains keys for 24 hours, not forever. Acceptance is not delivery.
export async function attemptEmail(resend, row, now = Date.now()) {
  if (row.acceptedId) return { acceptedId: row.acceptedId, alreadyRecorded: true };
  const age = now - row.firstAttemptAt;
  // Stop 5 minutes early to allow for clock skew / requests in flight.
  if (!Number.isFinite(age) || age < 0 || age >= 23 * 3600000 + 55 * 60000) {
    throw new Error('reconcile_required: do not blindly resend after the 24-hour window');
  }
  if (!row.key || row.key.length > 256 || !row.payload) throw new Error('invalid_outbox_row');
  let response;
  try {
    response = await resend.emails.send(row.payload, { idempotencyKey: row.key });
  } catch {
    throw new Error('unknown_outcome: reconcile; bounded same-key retry only within the window');
  }
  const { data, error } = response;
  if (error) {
    if (error.name === 'invalid_idempotent_request') {
      throw new Error('payload_conflict: stop; do not mint a new key to bypass this 409');
    }
    if (error.name === 'concurrent_idempotent_requests') {
      throw new Error('in_progress: defer with bounded backoff and recheck the window');
    }
    throw new Error(`send_failed: ${error.name}; inspect before any retry`);
  }
  if (!data?.id) throw new Error('unknown_outcome: missing acceptance id; reconcile');
  return { acceptedId: data.id }; // Caller must durably save this before acking its job.
}
// On long outages, check durable state plus provider logs/webhooks before deciding
// whether to resend. A crash after acceptance but before saving the id is ambiguous.
// If reconciliation cannot resolve it, hold for review; this is not exactly-once delivery.
