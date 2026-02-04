import requests
import os
import sys
import shutil

SEPARATOR = "-----"
OUTPUT_DIR = "responses"
COMBINED_FILE = "all_responses.txt"

if len(sys.argv) != 2:
    print("Usage: python raw_request_replayer.py <raw_requests.txt>")
    sys.exit(1)

# ----------------------------
# Helpers
# ----------------------------

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

# ----------------------------
# Reset responses directory
# ----------------------------

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# Reset combined file (ONLY ONE)
# ----------------------------

with open(COMBINED_FILE, "w", encoding="utf-8") as f:
    f.write("")

print(f"[+] Using combined output file: {COMBINED_FILE}")

# ----------------------------
# Load input requests
# ----------------------------

with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as f:
    data = f.read()

requests_raw = [r.strip() for r in data.split(SEPARATOR) if r.strip()]

print(f"[+] Loaded {len(requests_raw)} requests")

if not requests_raw:
    print("[!] No requests found. Check separator '-----'")
    sys.exit(1)

# ----------------------------
# Replay + capture
# ----------------------------

with open(COMBINED_FILE, "a", encoding="utf-8") as combined:

    for idx, raw in enumerate(requests_raw, start=1):
        try:
            method, path, headers, body = parse_raw_request(raw)

            host = headers.get("Host")
            if not host:
                print("[!] Missing Host header, skipping")
                continue

            scheme = "https" if ":443" in host or headers.get("Origin", "").startswith("https") else "http"
            url = f"{scheme}://{host}{path}"

            headers.pop("Content-Length", None)

            resp = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=body if body else None,
                verify=False,
                timeout=20
            )

            filename = sanitize_filename(path) + ".txt"
            outfile = os.path.join(OUTPUT_DIR, filename)

            response_text = (
                f"HTTP {resp.status_code}\n"
                + "\n".join(f"{k}: {v}" for k, v in resp.headers.items())
                + "\n\n"
                + resp.text
            )

            # ----------------------------
            # Save individual response
            # ----------------------------
            with open(outfile, "w", encoding="utf-8") as out:
                out.write(response_text)

            # ----------------------------
            # Save REQUEST + RESPONSE together
            # ----------------------------
            combined.write(f"##### ITERATION {idx}\n")
            combined.write("===== REQUEST =====\n")
            combined.write(raw.strip() + "\n\n")
            combined.write("===== RESPONSE =====\n")
            combined.write(response_text)
            combined.write("\n\n------\n\n")

            print(f"[+] {method} {path} → saved")

        except Exception as e:
            print("[ERROR]", e)

print("[+] Done.")
