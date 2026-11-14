// Node 22+. Read-only data-source query, not a full workspace export.
// Pass a data_source_id, not a database_id, and a server-side token.
// Sequential calls only; concurrent jobs still need a shared rate-limit queue.
export async function queryAll(dataSourceId, token, {
  fetchImpl = fetch, sleep = ms => new Promise(r => setTimeout(r, ms)),
  random = Math.random, maxPages = 1000,
} = {}) {
  const results = [], seen = new Set();
  let cursor;
  for (let page = 0; page < maxPages; page++) {
    let body;
    for (let attempt = 0; ; attempt++) {
      const res = await fetchImpl(
        `https://api.notion.com/v1/data_sources/${encodeURIComponent(dataSourceId)}/query`,
        { method: 'POST', signal: AbortSignal.timeout(30000),
          headers: { Authorization: `Bearer ${token}`,
            'Notion-Version': '2026-03-11', 'Content-Type': 'application/json' },
          body: JSON.stringify({ page_size: 100, ...(cursor ? { start_cursor: cursor } : {}) }) });
      body = await res.json();
      if (res.ok) break;
      const blocked = body.additional_data?.rate_limit_reason === 'public_api_request_blocked';
      if (![429, 529].includes(res.status) || blocked || attempt >= 4) {
        throw new Error(`Notion HTTP ${res.status}: ${body.code ?? 'unknown_error'}`);
      }
      const raw = res.headers.get('Retry-After') ?? body.additional_data?.retry_after;
      const seconds = raw != null && /^\d+$/.test(String(raw)) ? Number(raw) : 0;
      const wait = Math.max(seconds * 1000, 1000 * 2 ** attempt) + random() * 250;
      // Never shorten a server wait: stop and let the caller reschedule instead.
      if (!Number.isFinite(wait) || wait > 300000) throw new Error('Retry wait exceeds 5 minutes; reschedule');
      await sleep(wait); // The loop retries the identical page, not the next cursor.
    }
    if (!Array.isArray(body.results) || typeof body.has_more !== 'boolean') {
      throw new Error('Invalid paginated response');
    }
    if (body.request_status?.type === 'incomplete') {
      throw new Error('Query capped at 10,000 results; partition the query');
    }
    results.push(...body.results);
    if (!body.has_more) return results;
    if (typeof body.next_cursor !== 'string' || !body.next_cursor || seen.has(body.next_cursor)) {
      throw new Error('Missing or repeated pagination cursor');
    }
    seen.add(body.next_cursor);
    cursor = body.next_cursor;
    await sleep(350);
  }
  throw new Error('Page limit reached; no complete result returned');
}
// Network/timeout/JSON errors propagate. No silent partial results.
// Live edits can alter pagination: this is not a transactionally consistent snapshot.
