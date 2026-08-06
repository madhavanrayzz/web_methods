# Feature

Inviting a User

---

# Official Documentation

(Paste the documentation here)

---

# Understanding

Explain each sentence in your own words.

---

# Mind Map

Invite User
    │
    ▼
Invitation Created
    │
    ▼
Pending Invitation
    │
 ┌──┴────────────┐
 │               │
 ▼               ▼
Accept        Reject
 │               │
 ▼               ▼
Organization   End
Member

---

# State Machine

Invitation Created
        │
        ▼
Pending
        │
        ▼
Accepted
        │
        ▼
Member

---

# Actors

- Organization Owner
- Invited User
- Organization
- Email Service

---

# Objects

- Invitation
- Organization
- User
- Role
- Policy

---

# Trust Boundaries

- Email
- Invitation Token
- Organization Membership

---

# Questions

## Flow

- Can Pending become Member directly?
- Can the invitation be reused?
- Can it expire while being accepted?

## Authorization

- Who can create an invitation?
- Who can revoke it?
- Who can resend it?

## Validation

- Is the email validated?
- Is the token unique?
- Is expiration checked?

---

# My Notes

...

---

# Future Testing Ideas

(Not testing now—just ideas to revisit later.)

---

# Recall Questions

1. What are all the states?
2. Who performs each action?
3. What transitions exist?
4. Which transition looks the weakest?
