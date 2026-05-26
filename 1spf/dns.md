What is Zone Transfer?

👉 Zone Transfer = copying all DNS records of a domain

Normally:

You → ask DNS → get 1 record (A, TXT, etc.)

But with zone transfer:

You → ask DNS → get EVERYTHING
📦 What “everything” means

If it works, you get:

- subdomains (api.domain.com, admin.domain.com)
- internal hosts
- mail servers
- IP addresses
- sometimes staging/dev systems

👉 Basically:

Full map of the domain
🔥 Why this is dangerous

Imagine instead of brute forcing subdomains:

You instantly get ALL of them

👉 That’s huge for:

attack surface discovery
finding hidden endpoints
internal services exposure
