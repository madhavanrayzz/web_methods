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




Example Explained
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
