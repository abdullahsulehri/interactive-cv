"""Copy content.json into the <script id="content-data"> block of index.html.
Edit text ONLY in content.json, then run:   python tools/sync_content.py
Check without writing (used by lint/CI):    python tools/sync_content.py --check"""
import json,re,sys,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
c=json.loads((root/'content.json').read_text(encoding='utf-8'))
h=(root/'index.html').read_text(encoding='utf-8')
pat=re.compile(r'(<script id="content-data" type="application/json">)(.*?)(</script>)',re.S)
m=pat.search(h)
if not m: sys.exit('content-data block not found in index.html')
emb=json.dumps(c,ensure_ascii=False).replace('</','<\\/')
if '--check' in sys.argv:
    same=json.loads(m.group(2))==c
    print('content in sync' if same else 'OUT OF SYNC: run python tools/sync_content.py');sys.exit(0 if same else 1)
(root/'index.html').write_text(h[:m.start(2)]+emb+h[m.end(2):],encoding='utf-8')
(root/'content.json').write_text(json.dumps(c,ensure_ascii=False,indent=1),encoding='utf-8')
print('index.html updated from content.json')
