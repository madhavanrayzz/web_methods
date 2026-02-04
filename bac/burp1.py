import xml.etree.ElementTree as ET
import base64
import sys

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} burp.xml")
    sys.exit(1)

tree = ET.parse(sys.argv[1])
root = tree.getroot()

for item in root.findall("item"):
    req = item.find("request")
    if req is None or not req.text:
        continue

    raw = req.text.strip()

    if req.attrib.get("base64") == "true":
        raw = base64.b64decode(raw).decode("utf-8", errors="ignore")

    raw = raw.strip()

    if not raw:
        continue

    print(raw)
    print("\n-----\n")
