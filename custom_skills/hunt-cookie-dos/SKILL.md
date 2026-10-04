---
name: hunt-cookie-dos
description: "Assess cookie-related denial-of-service risks in explicitly authorized web applications, with or without authentication. Check cookie/header size limits, cookie-count limits, duplicate-cookie parsing, cookie-setting and cookie-scope behavior, and attacker-controllable bulk inputs. Use conservative, bounded tests; distinguish local request rejection from cross-user/service availability impact; and save reproducible findings and evidence under a target-specific output folder."
compatibility: opencode
metadata:
  category: web-security
  workflow: authorized-pentest
---

# HUNT-COOKIE-DOS — Cookie-Related Denial of Service

## Mission

Find and validate realistic cookie-related availability weaknesses in the supplied, authorized application. Test unauthenticated and authenticated surfaces when available. Investigate whether attacker-controllable cookies or cookie-setting inputs can cause request rejection, victim-browser cookie accumulation, expensive server-side parsing/session work, cookie parsing ambiguity, or failures affecting more than one deliberately malformed request.

Do not assume every HTTP 400/431 is a vulnerability. A single oversized request rejected cleanly is usually a limit working as intended, not proof of DoS.

## Authorization and safety gates

1. Only test hosts, paths, accounts, and environments explicitly supplied as in scope by the user.
2. If scope or permission is unclear, perform passive review and ask for confirmation before active requests.
3. Use the least disruptive method that can answer the question. Start with normal requests and small boundary checks.
4. Do not flood endpoints, run stress/load tests, spray huge payloads, create thousands of cookies, automate repeated session invalidation, or attempt to make a production service unavailable.
5. Do not test cross-user impact against real users. Use a second test account or a dedicated test browser only when authorized.
6. If the application becomes slow, starts returning elevated errors, or shows signs of instability, stop immediately and record the last successful test.
7. Never put passwords, session cookies, bearer tokens, CSRF tokens, or personal data in findings, logs, command history, or generated reports. Redact secrets as `[REDACTED_SESSION]`.
8. Do not exfiltrate data. Availability testing does not require reading unrelated user data.

## Inputs and operating modes

Use whatever the user has provided; do not demand every field before beginning safe discovery.

- `TARGET`: base URL or list of in-scope URLs.
- `AUTH`: optional cookie jar/session file or explicitly supplied test-account session.
- `ENDPOINTS`: optional known paths or API routes.
- `BULK_INPUTS`: optional endpoints/fields accepting arrays, repeated parameters, imports, batch operations, or multi-value form fields.
- `OUTPUT_DIR`: user-provided output path, otherwise `findings/cookie-dos/<target-slug>/<UTC-timestamp>/`.

If no authenticated session is available, proceed with unauthenticated testing and mark authenticated checks `NOT TESTED — no authorized session supplied`. Do not obtain or guess credentials. If a session is available, use it only for in-scope testing and redact it from evidence.

## Core distinctions

### A. Oversized Cookie header
A request with a large `Cookie` header may receive `400`, `431`, `413`, a proxy error, or a connection close. Determine which component rejected it if possible. A consistent per-request rejection with no wider impact is normally expected defensive behavior.

### B. Cookie bomb / client-side cookie accumulation
An attacker may be able to make a victim's browser store many or large cookies for a target host/domain, causing later requests to exceed browser, proxy, CDN, web-server, or application limits. This is only plausible when there is a realistic way to plant cookies for the relevant domain. Do not create a large cookie bomb on production. Verify the cookie-setting primitive and limits with a small controlled test in a dedicated test profile or staging environment.

### C. Cookie parser or session-processing weakness
Duplicate cookie names, unusual encodings, or malformed values may be parsed inconsistently by a proxy, framework, and application. Look for demonstrable failures or excessive processing, not just differing values. Never alter another user's session.

### D. Bulk application inputs
If the app accepts mass values (large arrays, repeated form fields, batch IDs, import rows, or many cookie values), check for missing limits and disproportionate processing using small, stepped test sizes only. This is a separate resource-consumption path unless the input specifically controls cookie creation or processing. Do not jump straight to massive payloads.

## Workflow

### Phase 1 — Establish baseline
1. Confirm target URL and scope.
2. Identify a CDN, WAF, reverse proxy, load balancer, or API gateway when observable.
3. Record a normal response for a public route, a route that sets cookies, a session-dependent route if a test session exists, and a bulk-input route if identified.
4. Record status, response time, response size, relevant headers, and `Set-Cookie` names/attributes. Redact values.
5. Avoid broad crawling when the supplied target/endpoint list is sufficient.

### Phase 2 — Inventory cookie behavior
Review `Set-Cookie` and record cookie name (not value), number set, approximate value length, `Domain`, `Path`, `Expires`/`Max-Age`, `Secure`, `HttpOnly`, and `SameSite`. Determine whether cookies accumulate or are overwritten and whether user-controlled input affects cookie name, domain, path, or value. A missing cookie attribute is not a DoS finding by itself.

### Phase 3 — Bounded header-limit checks
Only on an explicitly authorized target, send a small progression of synthetic, non-secret cookie values. Suggested progression for a dedicated test environment: 1 KiB, 2 KiB, 4 KiB, then at most 8 KiB total `Cookie` header unless the owner explicitly approves a different limit. Count cookie names and separators in the total. Start with one request per size per endpoint; do not parallelize.

- Compare unauthenticated and authenticated routes if an authorized test session is available.
- If the first size causes errors or latency spikes, stop increasing.
- Do not infer that a real browser will store/send a value just because a raw HTTP client can send it.
- Record whether rejection is deterministic and whether ordinary requests still work immediately afterward.
- Do not keep increasing payload size to force failure or bypass configured limits.

### Phase 4 — Cookie count and duplicate-name checks
Using a few synthetic cookies, test a small count progression (for example 1, 5, 10, then 20 cookies) in staging or with owner approval. Test duplicate cookie names only where useful to determine parser precedence, using harmless values such as `testA` and `testB`. Compare proxy and application behavior only where logs/architecture details are legitimately available. Stop at the first sign of instability or shared impact.

A request receiving a normal 400/431 due to configured limits is not, by itself, reportable. Look for unsafe accumulation, bypass of a documented bound, crash/restart, persistent outage, or disproportionate work.

### Phase 5 — Cookie-setting / cookie-bomb assessment
1. Identify routes that set cookies based on user input, repeated actions, or untrusted content.
2. Determine whether each interaction adds a new cookie instead of overwriting an existing one.
3. Check whether cookie scope (`Domain`/`Path`) makes it accompany important requests.
4. Determine whether an attacker can realistically cause a victim to visit the cookie-setting route or control a sibling subdomain. Treat this as a hypothesis until proven.
5. In staging or a dedicated test browser, verify with a small number of cookies that the browser accepts them, sends them to the intended host/path, and the request header grows as expected.
6. Stop before approaching the application's header limit. Use measured growth and configured limits to estimate risk; do not cause real-user traffic to fail.
7. Describe unverified cross-user effects as limitations, not proven impact.

### Phase 6 — Bulk/mass-value input checks
If an endpoint accepts multiple values, arrays, batches, repeated parameters, file imports, or a multi-select:
1. Identify documented or obvious maximums and expected use.
2. Begin with a normal request, then small sizes such as 5, 10, and 20 items only where safe and meaningful.
3. Increase only if responses remain stable and the owner authorized further testing. Do not use unbounded or huge lists.
4. Compare response time and server behavior against baseline. One slow response is not enough to establish DoS.
5. Check whether validation rejects oversized batches early, whether limits apply consistently, and whether processing happens before validation.
6. Do not send repeated batches concurrently. Do not test expensive actions such as email/SMS dispatch, payments, account creation, or imports at scale.
7. If a small input produces a large and reproducible slowdown, stop and document it.
8. Report this as a separate resource-consumption finding unless it directly depends on cookie processing.

### Phase 7 — Optional authenticated checks
When an authorized test session exists, test only the user's own test account and minimum routes needed. Compare the same safe request with and without the session cookie. Check whether session parsing or lookup changes behavior. Never invalidate, overwrite, or tamper with another user's session. Store only a redacted request and minimum response evidence.

Without a session, continue public-route checks and explicitly list the authenticated coverage gap.

### Phase 8 — Validate actual impact
- **Informational / not a finding:** a large request is rejected cleanly; only the test request fails; configured limits behave as expected.
- **Potential Low:** weak cookie limits or unsafe accumulation is observed, but practical victim impact is not established.
- **Potential Medium:** a reproducible, realistic cookie-setting path causes a test browser's ordinary subsequent requests to fail, with clear prerequisites and no service-wide claim.
- **Potential High:** only consider if a safe, owner-approved test proves broad availability impact or severe shared failure, with strong evidence and no speculative assumptions. Never try to prove this by taking a live service down.

Severity must follow demonstrated impact, attacker prerequisites, affected scope, and program policy. Do not assign severity based solely on payload size or a 400/431 response.

### Phase 9 — Save findings and evidence
Create a target-specific directory:
`findings/cookie-dos/<target-slug>/<UTC-timestamp>/`

If the workspace already has an established findings structure, follow it rather than creating a conflicting tree. Create:

- `summary.md` — executive summary and result (`CONFIRMED`, `POTENTIAL`, `NOT VULNERABLE`, or `NOT TESTED`).
- `finding.md` — report using `templates/finding-report.md`.
- `evidence/requests-redacted.txt` — minimal relevant requests, with all secrets removed.
- `evidence/responses-redacted.txt` — status, relevant headers, and short excerpts with personal data removed.
- `test-matrix.csv` — endpoint, auth state, test type, bounded input size/count, status, latency, outcome, and notes.
- `limitations.md` — untested routes, unavailable authentication, production safety constraints, and assumptions.
- `metadata.json` — target, UTC timestamp, tools/versions if known, and user-supplied scope. Never include credentials.

Do not create a confirmed finding merely because the skill ran. If no issue is proven, save an assessment stating what was tested and what was not.

## Output quality rules
- Use exact URLs and observed response codes; do not invent endpoints, headers, or results.
- Separate observation, interpretation, and impact.
- Mark inferred effects as hypotheses.
- Include a minimal reproducible PoC only if safe and necessary. Keep it bounded and non-destructive.
- Include remediation: enforce reasonable total request-header/cookie size and count limits at edge and app; reject excessive input early; cap batch/list sizes; prevent untrusted input controlling cookie scope; overwrite stable cookie names instead of accumulating new names; align proxy/app limits; and fail gracefully.
- Never label a finding “DoS” without explaining who is affected, for how long, and what an attacker can realistically cause.
- Prefer staging reproduction over production availability testing.

## Reference material
Read `references/test-matrix.md` for test cases and stop conditions. Use `templates/finding-report.md` for report output. Use `scripts/init-finding.sh` only if a directory scaffold is useful; inspect it before running and pass a safe target slug.
