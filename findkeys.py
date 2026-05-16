#!/usr/bin/env python3
import json, csv, sys

IN='vault.json'   # change if your export has a different name
OUT='passkeys.csv'

try:
    with open(IN, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    sys.exit(f"Input file not found: {IN}")

with open(OUT, 'w', newline='', encoding='utf-8') as out:
    w = csv.writer(out)
    w.writerow(['id','name','username','uri','passkey_id','passkey_createdAt'])
    for it in data.get('items', []):
        creds = (it.get('login') or {}).get('fido2Credentials') or []
        for c in creds:
            uri = ''
            uris = (it.get('login') or {}).get('uris') or []
            if uris and isinstance(uris, list):
                uri = uris[0].get('uri','') if isinstance(uris[0], dict) else ''
            w.writerow([
                it.get('id',''),
                it.get('name',''),
                (it.get('login') or {}).get('username',''),
                uri,
                c.get('id',''),
                c.get('createdAt','')
            ])

print(f"Wrote {OUT}")
