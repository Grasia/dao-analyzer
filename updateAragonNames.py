import requests
import json
import re

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

processed_list = [_parse_item(x) for x in extracted_list]
print(json.dumps({"mainnet":processed_list}, indent=2))