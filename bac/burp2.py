import requests
import re
import os
import sys
from urllib.parse import urlparse

SEPARATOR = "-----"
OUTPUT_DIR = "responses"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(path):
    path = path.split("?", 1)
    base = path[0].strip("/").replace("/", "_")
    query = path[1].replace("&", "_").replace("=", "=") if len(path) > 1 else ""
    return f"{base}_{query}".strip("_") or "root"

def parse_raw_request(raw):
    lines = raw.strip().split("\n")
    request_line = lines[0].strip()
    method, path, _ = request_line.split(" ", 2)

    headers = {}
    body = ""

    i = 1
    while i < len(lines) and lines[i].strip():
        k, v = lines[i].split(":", 1)
        headers[k.strip()] = v.strip()
        i += 1

    body = "\n".join(lines[i+1:]).strip()
    return method, path, headers, body

with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as f:
    data = f.read()

requests_raw = [r.strip() for r in data.split(SEPARATOR) if r.strip()]

for raw in requests_raw:
    method, path, headers, body = parse_raw_request(raw)

    host = headers.get("Host")
    if not host:
        print("[!] Missing Host header, skipping")
        continue

    scheme = "https" if ":443" in host or headers.get("Origin", "").startswith("https") else "http"
    url = f"{scheme}://{host}{path}"

    filename = sanitize_filename(path)
    outfile = os.path.join(OUTPUT_DIR, f"{filename}.txt")

    headers.pop("Content-Length", None)

    resp = requests.request(
        method=method,
        url=url,
        headers=headers,
        data=body if body else None,
        verify=False
    )

    with open(outfile, "w", encoding="utf-8") as out:
        out.write(f"HTTP {resp.status_code}\n")
        out.write("\n".join(f"{k}: {v}" for k, v in resp.headers.items()))
        out.write("\n\n")
        out.write(resp.text)

    print(f"[+] {method} {path} → {outfile}")
