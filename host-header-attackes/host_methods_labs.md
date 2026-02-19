STEP-BY-STEP CHECKLIST (follow strictly)
STEP 1: Send baseline request
GET /example HTTP/1.1
Host: vulnerable-website.com


Confirm:

Normal response

Note redirects

Note absolute URLs

Note cookies

This is your control sample.

STEP 2: Inject duplicate Host headers
GET /example HTTP/1.1
Host: vulnerable-website.com
Host: evil.com


Send via:

Burp Repeater (mandatory)

Disable auto header cleanup

❌ Curl often normalizes this
❌ Browsers won’t allow it

STEP 3: Observe which Host is trusted

Check carefully:

Response body

Redirect Location header

Absolute links

CSP headers

Password reset links

Cache behavior

If you see:

https://evil.com/...


→ vulnerability confirmed.

If nothing changes → continue testing variants.

STEP 4: Reverse header order (critical)

Many people miss this.

GET /example HTTP/1.1
Host: evil.com
Host: vulnerable-website.com


Why this matters:

Some proxies use first

Some backends use last

Order matters. Always test both.

STEP 5: Test alternative host headers

Some stacks accept:

X-Forwarded-Host: evil.com
X-Host: evil.com
Forwarded: host=evil.com


Also test combinations:

Host: vulnerable-website.com
X-Forwarded-Host: evil.com
