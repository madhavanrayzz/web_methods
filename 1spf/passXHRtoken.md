Reset Token Leak — Mini Checklist
1. Trigger reset
Forgot password → submit email
2. Check Burp (MAIN step)
Proxy → HTTP History
Find: POST /forgot-password
Open Response

👉 Look for:

token
reset_token
jwt
3. If found
Copy token
Send to:
POST /reset-password (Burp Repeater)
Add new password

👉 If it works → 🔥 VULN CONFIRMED

4. If not found (backup checks)

A. DevTools

Network → XHR/Fetch
Check responses

B. JS files (last option)

Target → Site map
Disable filters (show .js)
Search: token, reset, jwt
