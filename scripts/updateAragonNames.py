#!/bin/env python
import requests
import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} filename", file=sys.stderr)
    exit(1)

PREV_FILE = Path(sys.argv[1])

# flake8: noqa W605
KNOWN_ORGS_FILE_URL="https://github.com/aragon/client/raw/develop/src/known-organizations/index.js"
REGEX_MAIN_DICT = re.compile("export\s+const\s+KnownOrganizations\s+=\s+{\s+main:[^\[]+\[([^\]]*)\]", re.MULTILINE)
REGEX_ITEM_DICT = {
    "address": re.compile("address:\s+'(0x[0123456789abcdefABCDEF]{0,40})'"),
    "domain": re.compile("domain:\s+'([\.\w]*)'"),
    "name": re.compile("name:\s+'([\w\s\.]+)'"),
} 
r = requests.get(KNOWN_ORGS_FILE_URL)

assert(r.status_code == 200)

extracted_list = re.findall("(\{[^\}]+\})," ,REGEX_MAIN_DICT.findall(r.text)[0], re.MULTILINE)

def _parse_item(item):
    return {k:v.findall(item)[0] for k,v in REGEX_ITEM_DICT.items()}

with open(PREV_FILE, 'r') as pf:
    prev_json = json.loads(pf.read())

processed_list = [_parse_item(x) for x in extracted_list]
processed_dict = {"mainnet": processed_list}

print(json.dumps(prev_json | processed_dict, indent=2))
