"""Static code + content checks (no browser, ~1s). Run before every publish:  python tools/lint.py
Rules: DESIGN-RULES.md section 10 (S1-S8). Counts in tools/lint-budget.json can go DOWN, never up.
After a clean-up lowers a count:  python tools/lint.py --lower-budget"""
import re,json,sys,subprocess,pathlib,tempfile,collections
root=pathlib.Path(__file__).resolve().parent.parent
H=(root/'index.html').read_text(encoding='utf-8')
budget_f=root/'tools'/'lint-budget.json';B=json.loads(budget_f.read_text())
E=[];W=[];N={}
def err(rule,msg):E.append(f'{rule}: {msg}')
# ---------- structure ----------
styles=re.findall(r'<style[^>]*>(.*?)</style>',H,re.S)
if len(styles)!=1: err('S1',f'{len(styles)} <style> blocks; keep exactly one')
css='\n'.join(styles)
body=re.sub(r'<script id="content-data".*?</script>','',H,flags=re.S)
scripts=[s for a,s in re.findall(r'<script(\s[^>]*)?>(.*?)</script>',body,re.S) if 'ld+json' not in (a or '')]
js='\n'.join(scripts)
nocomment=re.sub(r'/\*.*?\*/','',css,flags=re.S)
decls=re.findall(r'([\w-]+)\s*:\s*([^;{}]+)',re.sub(r'[^{}]*\{','{',nocomment))
# ---------- S1 cascade hygiene (ratchet) ----------
N['important']=css.count('!important')
sels=collections.Counter(re.sub(r'\s+',' ',s.strip()) for s in re.findall(r'([^{}@/][^{}]*?)\{',re.sub(r'@media[^{]*\{','',nocomment)) if not s.strip().startswith(':root'))
N['duplicate_selectors']=sum(1 for v in sels.values() if v>1)
N['setTimeout']=js.count('setTimeout')
N['inline_style_attrs']=len(re.findall(r'style="',body))
N['colour_literals_outside_root']=len(re.findall(r'#[0-9a-fA-F]{3,8}\b|rgba?\(',re.sub(r'(:root|\[data-[\w-]+[^\]]*\])[^{]*\{[^}]*\}','',nocomment)))
for k,v in N.items():
    if v>B.get(k,0): err('S1',f'{k} = {v}, budget {B.get(k,0)}. Fix the cause (specificity/order/tokens) instead of adding more.')
# ---------- S2 tokens ----------
for p,v in decls:
    v=v.replace('!important','').strip()
    if p=='z-index' and not v.startswith('var(--z-') and v not in('auto','0'): err('S2',f'z-index: {v} -> use a --z-* token')
    if p=='border-radius' and not re.fullmatch(r'(var\(--r[\w-]*\)\s*)+|0|inherit|none',v): err('S2',f'border-radius: {v} -> use --r / --r-* tokens')
# ---------- S3 type scale (T4) ----------
SCALE={'11','12','13','14','15','16','18','20','24'};EXC={'0':'hidden label','9.5':'dot-to-pill micro label (exception)','34':'loader monogram (exception)','64':'testimonial quote mark glyph (exception)'}
sizes=[v for p,v in decls if p=='font-size']+[m for p,v in decls if p=='font' and not re.search(r'clamp|calc',v) for m in re.findall(r'(?:^|\s)([\d.]+)px',v)]
for v in sizes:
    v=v.replace('!important','').strip()
    if re.search(r'clamp|calc|var|em\b|rem|%|inherit',v): continue
    n=v.replace('px','')
    if n not in SCALE and n not in EXC: err('S3',f'font-size {v} is off the T4 scale (11 12 13 14 15 16 18 20 24)')
# ---------- S4 motion (M1, M2) ----------
OKDUR={'.2s','0.2s','.4s','0.4s','1.2s','0s','0ms'};EXCDUR={'2.4s':'loader pulse loop (exception)'}
for p,v in decls:
    if p not in('transition','animation') or v.strip().startswith('none'): continue
    for seg in re.split(r',(?![^()]*\))',v):
        for d in re.findall(r'(?<![\w.(-])(\d*\.?\d+m?s)\b',seg):
            if d not in OKDUR and d not in EXCDUR: err('S4',f'{p}: "{seg.strip()}" uses {d}; speeds are .2s / .4s / 1.2s')
        if 'var(--ez)' not in seg and not re.search(r'steps\(',seg): err('S4',f'{p}: "{seg.strip()}" has no var(--ez)')
# ---------- S5 breakpoints ----------
OKMQ={'(min-width:900px)','(max-width:899.98px)','(hover:none)','(hover:hover)','(min-width:1200px)','(max-width:560px)','(min-width:900px) and (max-width:1180px)','(prefers-reduced-motion:reduce)','(min-width:1100px)','(max-width:380px)','(min-width:900px) and (max-width:1199.98px)'}
for mq in re.findall(r'@media\s*([^{]+)\{',css):
    if mq.strip() not in OKMQ: err('S5',f'@media {mq.strip()} not in the breakpoint list (laptop starts at 900px; phone is max-width:899.98px)')
# ---------- S6 content ----------
r=subprocess.run([sys.executable,str(root/'tools'/'sync_content.py'),'--check'],capture_output=True,text=True)
if r.returncode: err('S6','content.json and the copy inside index.html differ: run python tools/sync_content.py')
C=json.loads((root/'content.json').read_text(encoding='utf-8'))
def strings(o):
    if isinstance(o,str): yield o
    elif isinstance(o,dict):
        for k,v in o.items():
            if not k.startswith('_') and k not in('settings',): yield from strings(v)
    elif isinstance(o,list):
        for v in o: yield from strings(v)
text='\n'.join(strings(C))
UK={r'\b(optimi|organi|standardi|prioriti|customi|utili|recogni|summari|finali|speciali|monetis|visuali)s(e|ed|es|ing|ation|ations)\b':'-ize',r'\banalys(e|ed|es|ing)\b':'analyze',r'\bbehaviour\b':'behavior',r'\bcentre\b':'center',r'\bfavourite\b':'favorite',r'\bprogramme\b':'program'}
OFFICIAL=['Brand and Behaviour']  # official certificate/course titles keep their spelling
for o in OFFICIAL: text=text.replace(o,'')
for uk,us in UK.items():
    for m in re.finditer(uk,text,re.I): err('S6',f'US spelling: "{text[max(0,m.start()-25):m.end()+10].strip()}" ({uk}->{us})')
if re.search(r'\bMOT\b',text): err('S6','banned wording (rule D3): MOT')
if re.search('chartered accountant',json.dumps(C.get('education',''),ensure_ascii=False),re.I): err('S6','"chartered accountant" in education (rule D3)')
for pj in C.get('panels',{}).get('ai',{}).get('projects',[]):
    if len(pj.get('tags',[]))!=2: err('S6',f'AI card "{pj.get("title")}" has {len(pj.get("tags",[]))} tags; exactly 2 (rule D2)')
for t in (C.get('testimonials',{}) or {}).get('items',[]):
    if re.search(r'\b(19|20)\d\d\b',json.dumps(t)): err('S6',f'testimonial "{t.get("name")}" contains a year (rule D1)')
# ---------- F focus system ----------
FON_OK={'.act:first-child.f-on .pa .pi,.act:first-child:hover .pa .pi','.xr.f-on h3::before,.edc.f-on b::before','.mdb.f-on i','.logo.f-on .lgc,.tool.f-on .lgc,.logo:hover .lgc,.tool:hover .lgc','.logo.f-on img,.tool.f-on img,.logo:hover img,.tool:hover img','.cc.f-on .node','.cm.f-on .cm-dot','.sch button:hover .sd,.sch.f-on .sd'}
for s in re.findall(r'([^{}@/][^{}]*?)\{',re.sub(r'@media[^{]*\{','',nocomment)):
    s=re.sub(r'\s+',' ',s.strip())
    if '.f-on' in s and s not in FON_OK: err('F8',f'new focus style "{s}": highlights must use the one-dot system (dot fill or pill) - see DESIGN-RULES section 11')
if 'class=\"pa\" ' in H and '<span class=\"pi\">' not in H: err('F3','action pills must wrap icon + label in <span class="pi">')
for m in re.finditer(r'<(?:a|button) class="pa[^"]*"[^>]*>(?!<span class="pi">)',body): err('F3',f'pill without .pi wrapper: {m.group(0)[:60]}')
# ---------- S7 hygiene ----------
for mk in [r'/\*[^*]*test layer',r'/\*[^*]*round \d',r'TODO',r'FIXME',r'console\.log',r'debugger']:
    if re.search(mk,body,re.I): err('S7',f'leftover marker in index.html: {mk}')
for ref in sorted(set(re.findall(r'(?<![\w-])(?:assets|cv)/[\w\-./]+\.(?:webp|svg|png|jpg|jpeg|pdf|woff2)',H))):
    if not (root/ref).exists(): err('S7',f'missing file: {ref}')
with tempfile.TemporaryDirectory() as d:
    for i,s in enumerate(scripts):
        f=pathlib.Path(d)/f's{i}.js';f.write_text(s,encoding='utf-8')
        r=subprocess.run(['node','--check',str(f)],capture_output=True,text=True)
        if r.returncode: err('S7',f'JavaScript syntax error in script {i}: {r.stderr.strip().splitlines()[-1]}')
# ---------- report ----------
print('counts:',', '.join(f'{k} {v}/{B.get(k)}' for k,v in N.items()))
if '--lower-budget' in sys.argv and not E:
    nb={k:min(v,B.get(k,v)) for k,v in N.items()};budget_f.write_text(json.dumps(nb,indent=1));print('budget lowered:',nb)
if E:
    print(f'LINT FAILED ({len(E)})');[print(' -',e) for e in E[:60]];sys.exit(1)
print('LINT PASS')
