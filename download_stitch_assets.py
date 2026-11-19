import re
import urllib.request
import os

with open('stitch_lumina_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

urls = list(set(re.findall(r'https://lh3\.googleusercontent\.com/[^\s"\'<>]+', text)))
print('Found image URLs:', len(urls))
for i, u in enumerate(urls):
    print(f'[{i}] {u[:80]}...')
    out_name = f'assets/images/stitch_asset_{i}.png'
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            with open(out_name, 'wb') as out_f:
                out_f.write(content)
            print(f'Downloaded {out_name} ({len(content)} bytes)')
    except Exception as e:
        print(f'Failed {out_name}: {e}')
