# Cookie-Related Availability Finding

## Title
[Component/endpoint] — [specific cookie/header/input behavior] causes [demonstrated availability impact]

## Status
CONFIRMED / POTENTIAL / NOT VULNERABLE / NOT TESTED

## Severity
[Severity] — justify using proven impact and attacker prerequisites.

## Affected asset
- URL:
- Method:
- Environment:
- Authentication: Unauthenticated / Authorized test account / Not tested

## Summary
Describe observed behavior in 2–4 sentences. Separate confirmed facts from hypotheses.

## Preconditions
- Attacker capabilities:
- Victim interaction required:
- Authentication required:
- Scope restrictions:

## Steps to reproduce
1. Establish the normal baseline.
2. Send the bounded, synthetic test input.
3. Record the observed response.
4. Send one normal request to verify recovery, if safe.

Do not include credentials, session cookies, personal data, or destructive payloads.

## Expected result
The application should enforce consistent cookie/header and bulk-input limits, reject excessive inputs early, and remain available to other users.

## Actual result
Include observed behavior only: status codes, relevant redacted headers, response timing, error text, and recovery behavior.

## Impact
- Proven impact:
- Not proven / limitations:
- Who is affected:
- Duration/recovery:
- Realistic attacker prerequisites:

## Evidence
- `evidence/requests-redacted.txt`
- `evidence/responses-redacted.txt`
- `test-matrix.csv`

## Root-cause hypothesis
Label as a hypothesis unless supported by implementation details or server logs.

## Remediation
- Apply consistent total request-header and cookie size/count limits at the edge and application.
- Validate limits before expensive parsing, session lookups, or downstream work.
- Enforce maximum lengths and counts for bulk inputs and arrays.
- Prevent untrusted input from controlling cookie names or broad `Domain` scope.
- Overwrite stable cookie names rather than accumulating unique cookies.
- Align proxy and application limits and fail gracefully.
- Add monitoring/rate limits where appropriate, without treating rate limiting as a substitute for input bounds.

## Test coverage and limitations
- Routes tested:
- Sizes/counts tested:
- Auth coverage:
- Tests deliberately not run for safety:
- Remaining questions:
