# AWS Lambda vs Cloudflare Workers — a 2026 cost teardown

> One hundred million requests that each take 200 ms and use 10 ms of CPU cost $147.80 on AWS Lambda and $51.40 on Cloudflare Workers. Nothing about the code differs. One vendor bills the waiting.

*Prices verified 2026-11-10. Category: Serverless & Edge. Author: DevTeardown Team.*

## Verdict

For a request that waits, Workers is two to three times cheaper and the gap grows with every millisecond you spend on a database call. For a request that works, the two converge, and Lambda's free tier and memory ceiling win back the low end. The bill is a statement about your code's shape, not about the vendors' rates.

## 1. Two vendors, three meters, two definitions of work

Lambda now publishes two price sheets. Event Functions bill requests plus duration in GB-seconds: $0.0000133334 per GB-second on Arm, $0.0000166667 on x86, and $0.20 per million requests. Web Functions bill active CPU at $0.0000276944 per vCPU-second, memory at $0.0000036667 per GB-second for as long as the environment exists, and $0.30 per million requests.

Workers bill one thing that matters: CPU milliseconds, $0.02 per million after 30 million included, plus $0.30 per million requests after 10 million on a $5 plan. The page is explicit that there is no charge for duration, for egress or for bandwidth.

| Meter | Lambda Event | Lambda Web | Workers |
|---|---|---|---|
| Requests | $0.20/M | $0.30/M | $0.30/M |
| Duration | GB-seconds | memory GB-s, whole life | none |
| CPU | inside duration | $0.0000276944/vCPU-s | $0.02/M CPU-ms |

## 2. A GB-second is a memory meter wearing a clock

Duration billing multiplies wall time by allocated memory, and both factors are yours to set. A 512 MB function that takes 200 ms bills 0.5 GB × 0.2 s = 0.1 GB-s per request. At 100 million requests that is 10 million GB-seconds, or $133.34 on Arm at $0.0000133334.

Workers bills the 10 ms of actual work instead: 100 million × 10 ms = 1,000 million CPU-milliseconds, which is 970 million after the 30 million included, at $0.02 per million CPU-ms = $19.40.

So the ratio between the two vendors is not a rate difference. It is the fraction of the request that is CPU: 10 ms of 200 ms is 5%, and that 5% is what Workers meters. Make the handler heavier and the gap narrows; make it wait on a database and the gap widens.

## 3. The bills cross at about 7.5 million requests

Same shape everywhere below: 200 ms duration, 512 MB, 10 ms of CPU, one function.

| Requests/month | Lambda Event (Arm) | Workers | Cheaper |
|---|---|---|---|
| 5M | $0.80 + $1.33 = $2.13 | $5.00 + $0.40 = $5.40 | Lambda |
| 7.5M | $1.30 + $4.67 = $5.97 | $5.00 + $0.90 = $5.90 | Workers, by 7¢ |
| 10M | $1.80 + $8.00 = $9.80 | $5.00 + $1.40 = $6.40 | Workers |
| 50M | $9.80 + $61.33 = $71.13 | $5.00 + $12.00 + $9.40 = $26.40 | Workers |
| 100M | $19.80 + $128.00 = $147.80 | $5.00 + $27.00 + $19.40 = $51.40 | Workers |

The crossover is a free-tier artefact, not a policy: 1 million requests and 400,000 GB-seconds are free on Lambda, and 30 million CPU-ms are free on Workers. Below roughly 7.5 million requests the Lambda allowance is worth more than the CPU savings. Above it, the $5 plan floor disappears into the noise.

## 4. Lambda's second sheet splits the same request in two

Web Functions are AWS's answer to active-CPU billing, and they price the same 100 million requests differently.

| Line | Lambda Event | Lambda Web | Workers |
|---|---|---|---|
| Requests | $19.80 | $30.00 | $27.00 |
| Compute | 10M GB-s = $128.00 | 1M vCPU-s = $27.69, 1.296M GB-s = $4.75 | 970M CPU-ms = $19.40 |
| Plan floor | — | — | $5.00 |
| **Total** | **$147.80** | **$62.45** | **$51.40** |

Web Functions bill $62.45 for the same traffic, 42% of the Event price, and still 21% above the Workers bill. The memory meter is why: it bills the environment for its whole life, idle time included, and AWS's own examples quietly assume exactly one environment stays up for the entire month.

## 5. Where Lambda wins on the same sheet

The free tier, for one. Five million requests a month cost $2.13 on Lambda and $5.40 on Workers, and a hobby project that sends three million costs $2.73 by AWS's own worked example.

Memory ceiling is the second. Lambda allocates up to 10,240 MB per function, which covers a model that will not fit in a V8 isolate. Workers caps a single invocation at 5 minutes of CPU, 30 seconds by default.

The third is everything around the function: VPC access, IAM, SQS, Kinesis, Step Functions and the rest of the event-source catalogue. On an AWS shop, the compute line is frequently cheaper than the integration you would rewrite to leave it.

## 6. The exit door has a rewrite behind it

Workers runs JavaScript on V8 with a fetch-shaped API. A Lambda handler that imports a native module, spawns a process or needs a writable filesystem does not run there, and the 5-minute CPU cap is not negotiable with a support ticket.

The reverse move is easier and still not free: Workers' egress is $0 and Lambda's is not, so a byte-heavy service that moves back to Lambda picks up a data transfer line it never had.

Price the traffic, not the platform. If your p50 request spends most of its time waiting on a database, the CPU meter is the cheaper meter and the rewrite is the only real cost. If your requests are heavy, synchronous and mostly compute, the two bills converge and the free tier decides.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 100M requests at 200 ms, 512 MB, 10 ms CPU | Lambda Event Arm: 100M × 0.2 s × 0.5 GB = 10M GB-s, minus 400k free = 9.6M × $0.0000133334 = $128.00, plus 99M × $0.20/M = $19.80. Workers: (100M − 10M) × $0.30/M = $27.00, plus (1,000M − 30M) CPU-ms × $0.02/M = $19.40, plus $5.00 | $147.80 on Lambda against $51.40 on Workers |
| The same traffic on Lambda Web Functions | 100M × 10 ms = 1M vCPU-s × $0.0000276944 = $27.69; 0.5 GB × 2,592,000 s = 1,296,000 GB-s × $0.0000036667 = $4.75; 100M × $0.30/M = $30.00 | $62.45, 58% below Lambda's own Event price for identical traffic |
| Cross-over against Lambda's free tier | Lambda: (R − 1M) × $0.20/M + (R × 0.1 − 400k) × $0.0000133334. Workers: $5 + (R × 10 − 30M) × $0.02/M | Equal at about 7.5M requests a month; below that Lambda's free allowance wins, above it the CPU meter does |
| Replacing a 200 ms wait with a 1 s wait | At 10M requests: Lambda 10M × 1 s × 0.5 GB = 5M GB-s − 400k = 4.6M × $0.0000133334 = $61.33 + $1.80. Workers CPU is unchanged at 10M × 200 ms = 2,000M − 30M × $0.02/M = $39.40 + $5 | $63.13 against $44.40: the slower request costs Lambda $53 more and Workers nothing |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| Under about 5 million requests a month | Lambda Event Functions | The 1M-request and 400,000 GB-second free allowances cover the whole job: 5M requests at 200 ms and 512 MB price at $2.13 against $5.40 on Workers. |
| 100 million requests that mostly wait on I/O | Workers | The same shape prices at $51.40 against $147.80, because 10 ms of CPU out of a 200 ms request is all Workers meters. |
| A function that needs 10 GB of memory | Lambda | Lambda allocates up to 10,240 MB; Workers caps a single invocation at 5 minutes of CPU and runs in an isolate with a far smaller footprint. |
| Long-lived streaming to a browser | Lambda Web Functions | Active-CPU billing ignores the wait: AWS's own LLM streaming example prices 5M requests of 3 s at $33.94, against $101.00 as Event Functions. |
| Byte-heavy responses at the edge | Workers | Workers charges nothing for egress or bandwidth, and static asset requests are free and unlimited. |
| SQS, Kinesis, VPC and IAM already wired into the app | Lambda | The compute line is often the small one; rewriting event sources and IAM to leave AWS costs more than the difference on the invoice. |
| A cron job every hour, minutes of CPU each | Workers | Cloudflare's own example prices 720 invocations at 180,000 ms CPU each at $6.99, and duration is not a meter at all. |
| Traffic so spiky that one environment cannot serve it | Lambda Event Functions | Web Functions bill memory for the life of every environment, and the pricing examples quietly assume exactly one environment runs all month. |

## Migration path

Lambda to Workers is a runtime rewrite: the handler becomes a fetch listener, environment variables become bindings, and anything that needs a native module, a spawned process or a writable disk has no equivalent. State moves to Durable Objects or KV, which bill separately.

Workers to Lambda is smaller but not free: package the code, replace KV and Durable Objects with a database, and accept that egress is metered again. In both directions the traffic analysis comes first, because the arithmetic only favours one vendor when you know the request duration and the CPU share of it.

## Questions that change the decision

**Does Workers really charge nothing for duration?**  
The pricing page states there is no charge or limit for duration and no charge for data transfer or bandwidth. Only CPU milliseconds and requests are metered.

**What are Lambda Web Functions?**  
A second Lambda billing model that charges per request, per vCPU-second of active CPU and per GB-second of memory for as long as the execution environment exists.

**Which free tier is bigger?**  
Lambda's, in dollar terms at low volume: 1 million requests and 400,000 GB-seconds against Workers' 10 million requests and 30 million CPU-milliseconds on the $5 plan.

**Is a cold start billed?**  
On Event Functions the initialisation runs inside the billed duration, and SnapStart adds its own cache and restore charges. Workers does not bill duration at all.

## Sources

- https://aws.amazon.com/lambda/pricing/
- https://developers.cloudflare.com/workers/platform/pricing/
- https://developers.cloudflare.com/workers/platform/limits/
- https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
- https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html

## Same task, two SDKs

**AWS Lambda**

```
// Event Function: the meter starts at invocation and runs through the wait.
export const handler = async (event) => {
  const user = await db.users.findUnique({ where: { id: event.userId } }); // 180 ms here
  const digest = render(user);                                            // 10 ms here
  return { statusCode: 200, body: digest };
};
// Breaks when: the lookup takes 1 s. You are billed 1.01 s of 512 MB, so the wait
// is 99% of the invoice. Web Functions bill only the 10 ms of active CPU.
```

**Cloudflare Workers**

```
// Workers: nothing here is billed by the clock, only the CPU this code burns.
export default {
  async fetch(request, env) {
    const userId = new URL(request.url).searchParams.get("id");
    const user = await env.DB.prepare("SELECT * FROM users WHERE id = ?")
      .bind(userId).first();            // 180 ms of waiting, not billed
    return new Response(render(user), {
      headers: { "content-type": "text/html" },
    });
  },
};
// Breaks when: render() parses a 5 MB XML feed on every request. CPU is the meter,
// and the 30M CPU-ms allowance is 30 million milliseconds of exactly that.
```
