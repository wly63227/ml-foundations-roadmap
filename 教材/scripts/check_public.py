"""Check the deployed project prefix, all authored pages, and expected commit.

Run from the repository root after Actions succeeds:
python 教材/scripts/check_public.py --expected-commit COMMIT_SHA
Optional --external checks selected Markdown external URLs; failures stay visible.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--expected-commit', required=True)
parser.add_argument('--base', default='https://wly63227.github.io/ml-foundations-roadmap/')
parser.add_argument('--external', action='store_true')
args = parser.parse_args()
base = args.base.rstrip('/')+'/'
root = Path(__file__).resolve().parents[1]
def get(url):
    for attempt in range(1, 4):
        try:
            request = Request(url, headers={'User-Agent': 'ml-foundations-roadmap-release-check'})
            with urlopen(request, timeout=30) as response:
                return {'url': url, 'status': response.status, 'attempts': attempt, 'data': response.read()}
        except (HTTPError, URLError, TimeoutError) as exc:
            result = {'url': url, 'status': getattr(exc, 'code', None), 'attempts': attempt, 'error': str(exc)}
            if result['status'] not in (None, 429, 502, 503, 504) or attempt == 3:
                return result
            time.sleep(.5*attempt)

version = get(base+'version.json')
if version.get('status') != 200:
    raise SystemExit(f'Cannot read deployed version: {version}')
metadata = json.loads(version['data'])
if metadata['commit'] != args.expected_commit or metadata['dirty'] is not False:
    raise SystemExit(f'Unexpected deployed version: {metadata}')
pages = sorted((root/'docs').rglob('*.md'))
urls = [base+str(p.relative_to(root/'docs')).replace('\\','/').removesuffix('.md')+'.html' for p in pages]
urls += [base+'assets/style.css', base+'assets/app.js', base+'assets/roadmap.svg', base+'assets/katex/katex.min.css']
if args.external:
    urls += sorted(set(url for p in pages for url in re.findall(r'\]\((https://[^\s)]+)\)', p.read_text(encoding='utf-8')) if not url.startswith(base)))
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(get, urls))
for result in results:
    data = result.pop('data', None)
    if data is not None and result['url'].startswith(base) and result['url'].endswith('.html'):
        result['has_main'] = b'id="content"' in data
errors = [r for r in results if r.get('status') != 200 or r.get('has_main') is False]
report = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'version': metadata, 'results': results, 'errors': errors}
(root/'reports').mkdir(exist_ok=True)
(root/'reports/public.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'commit': metadata['commit'], 'urls': len(results), 'errors': errors}, ensure_ascii=False))
if errors:
    raise SystemExit(1)
