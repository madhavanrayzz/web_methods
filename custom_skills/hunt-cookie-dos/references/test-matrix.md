# Cookie DoS Test Matrix

Use only in explicitly authorized environments. This is a checklist, not a prompt to maximize payload size or disrupt a service.

| Test family | Safe initial check | Observe | Stop condition | Common false positive |
|---|---|---|---|---|
| Baseline | One ordinary request per route | Status, latency, response size, cookie names | Unexpected instability | Baseline route naturally slow |
| Header size | Synthetic values at 1, 2, 4 KiB; max 8 KiB total in staging unless approved | 400/431, proxy vs app behavior, recovery on next normal request | First error/latency spike | Correct rejection of an oversized request |
| Cookie count | 1, 5, 10, then 20 synthetic cookies in staging/approved test | Header growth, status, response latency | First instability | Header-size limit working correctly |
| Duplicate names | Two harmless values with same name | Which value proxy/app reads; errors | Any session/state effect or instability | Defined parser precedence with no impact |
| Cookie accumulation | Observe normal Set-Cookie behavior; small test browser only | New cookie per interaction vs overwrite, Domain/Path scope | Before approaching header limits | Browser-specific quota or unrelated cookie |
| Authenticated route | Same safe request with test session and without it | Difference in parsing, lookup, error behavior | Session disruption or side effects | Login required/401 by design |
| Bulk input | Baseline then 5, 10, 20 items on harmless endpoint | Validation, response time, resource behavior | Reproducible slowdown or errors | Expected proportional work |
| Malformed encoding | A few harmless malformed or encoded values | Graceful rejection vs exception | Any instability | Single 400/422 response |
| Recovery | One normal request after test | Service returns to baseline | If not recovered, stop and notify owner | Transient network issue |

## Minimum evidence
- Exact in-scope URL and method.
- Auth state (never include secrets).
- Baseline and test status codes and response times.
- Bounded input size/count and whether tested once or more.
- Whether normal requests recovered immediately.
- Attacker prerequisites for planting cookies or sending input.
- Scope of impact proven versus hypothesized.
- Why this is not simply a configured limit working as intended.

## Never do
- No unbounded loops, concurrency, payload floods, or thousands of cookies.
- Do not target other users' sessions.
- Do not trigger bulk email/SMS, payments, mass account creation, or expensive imports.
- Do not continue increasing sizes after an error or latency spike.
- Do not claim service-wide DoS from one rejected request.
