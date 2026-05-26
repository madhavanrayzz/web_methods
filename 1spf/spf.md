EMAIL CHECK – SIMPLE REFERENCE

1. CHECK SPF
dig TXT domain.com +short

Look for:
v=spf1 ...

Meaning:
include:xyz.com → allowed sender
ip4:x.x.x.x     → allowed IP
mx              → allowed mail server

-all  → block others (strong)
~all  → soft fail (weak)
+all  → allow all (broken)


2. CHECK DMARC
dig TXT _dmarc.domain.com +short

Look for:
v=DMARC1; p=...

Meaning:
p=none        → no protection
p=quarantine  → goes to spam
p=reject      → blocked


3. CORE RULE
DMARC = PASS if SPF OR DKIM passes
DMARC = FAIL if both fail


4. REAL VULNERABILITY

You must prove:
- spoof email sent
- lands in INBOX
- SPF: FAIL
- DKIM: FAIL
- DMARC: none / weak

→ THEN valid bug


5. NOT A VULN

- only SPF weak ❌
- only DMARC missing ❌
- email goes to spam ❌


6. SUBDOMAIN CHECK

dig TXT _dmarc.sub.domain.com +short

if empty → uses parent DMARC

look for:
sp=none → subdomains weak


FINAL MEMORY:
SPF = who can send
DMARC = what happens if they fail
