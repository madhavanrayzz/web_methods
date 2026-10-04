#!/usr/bin/env bash
set -euo pipefail

# Creates a finding scaffold only. It does not send requests or test a target.
if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <safe-target-slug> [output-root]" >&2
  exit 2
fi

slug="$1"
root="${2:-findings/cookie-dos}"
if [[ ! "$slug" =~ ^[A-Za-z0-9._-]{1,100}$ ]]; then
  echo "Target slug must use only letters, numbers, dot, underscore, or hyphen." >&2
  exit 2
fi

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
out="${root}/${slug}/${timestamp}"
mkdir -p "$out/evidence"
: > "$out/evidence/requests-redacted.txt"
: > "$out/evidence/responses-redacted.txt"
cat > "$out/summary.md" <<'SUMMARY_EOF'
# Cookie DoS Assessment

Status: NOT TESTED

Replace this with observed results only. Do not claim a vulnerability without evidence.
SUMMARY_EOF
cat > "$out/test-matrix.csv" <<'CSV_EOF'
endpoint,auth_state,test_type,input_size_or_count,status,latency_ms,outcome,notes
CSV_EOF
cat > "$out/limitations.md" <<'LIMIT_EOF'
# Limitations

- Scope/authorization:
- Authentication unavailable:
- Routes not tested:
- Production safety limits:
- Assumptions:
LIMIT_EOF
cat > "$out/metadata.json" <<JSON_EOF
{
  "target_slug": "${slug}",
  "created_utc": "${timestamp}",
  "finding_type": "cookie-related-availability",
  "secrets_included": false
}
JSON_EOF
echo "Created finding scaffold: $out"
