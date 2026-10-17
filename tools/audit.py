"""Layout audit for the CV site (rule Q1 in DESIGN-RULES.md).
Usage: pip install playwright && playwright install chromium
       python tools/audit.py [URL]   (default: the live site)
"""
import asyncio,json,sys
URL=sys.argv[1] if len(sys.argv)>1 else 'https://abdullahsulehri.github.io/interactive-cv/'
from playwright.async_api import async_playwright
JS=r'''()=>{const vis=e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'&&+s.opacity>0.05};
const all=[...document.querySelectorAll('body *')].filter(e=>!e.closest('#pnl')&&!e.closest('.xo'));
const clip=[],clamp=[];
for(const e of all){if(!vis(e))continue;const s=getComputedStyle(e);if(!e.textContent.trim())continue;const ov=/(hidden|clip)/.test(s.overflow+s.overflowX+s.overflowY);if(!ov)continue;
 const lc=s.webkitLineClamp&&s.webkitLineClamp!=='none';const cut=e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2;
 if(cut){const id=(e.id?'#'+e.id:'')+'.'+[...e.classList].join('.');(lc?clamp:clip).push(id+' «'+e.textContent.trim().slice(0,30)+'»')}}
const btnSel='button,a.btn,.btn,.pa,.nb,.hbwa,.hbt,.chip,.sch button,.mdb';const sig={};
for(const e of document.querySelectorAll(btnSel)){if(!vis(e))continue;const s=getComputedStyle(e);const k=[Math.round(parseFloat(s.height)),s.borderRadius,s.fontSize,s.fontWeight,s.borderTopWidth].join('/');const c=(e.className||e.tagName).toString().split(' ')[0]||e.tagName;sig[c]=sig[c]||new Set();sig[c].add(k)}
const fonts={},cols={},dur={};
for(const e of all){if(!vis(e))continue;const s=getComputedStyle(e);const t=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());if(t){const k=s.fontSize+' '+s.fontWeight;fonts[k]=(fonts[k]||0)+1;cols[s.color]=(cols[s.color]||0)+1}
 for(const d of (s.transitionDuration+','+s.animationDuration).split(','))if(d.trim()!=='0s')dur[d.trim()]=(dur[d.trim()]||0)+1}
const small=[];if(innerWidth<900){for(const e of document.querySelectorAll('a,button,input,select,textarea')){if(!vis(e))continue;const r=e.getBoundingClientRect();if(r.width<40||r.height<40)small.push(((e.className||e.tagName)+'').split(' ')[0]+' '+Math.round(r.width)+'x'+Math.round(r.height))}}
const offR=[...document.querySelectorAll('.wrap *, .hero *')].filter(e=>vis(e)&&!e.closest('#pnl')&&e.getBoundingClientRect().right>innerWidth+1&&getComputedStyle(e).position!=='fixed').map(e=>((e.className||e.tagName)+'').split(' ')[0]).slice(0,8);
const hc=[];for(const h of document.querySelectorAll('h1,h2,h3,.h1')){if(!vis(h))continue;const r=document.createRange();r.selectNodeContents(h);const tr=r.getBoundingClientRect();let p=h;while(p&&p!==document.body){const s=getComputedStyle(p);if(/(hidden|clip)/.test(s.overflow+s.overflowX+s.overflowY)){const pr=p.getBoundingClientRect();if(tr.left<pr.left-.5||tr.right>pr.right+.5||tr.top<pr.top-.5||tr.bottom>pr.bottom+.5){hc.push(h.textContent.trim().slice(0,24));}break}p=p.parentElement}}
const ic=[];for(const e of document.querySelectorAll('.pa .ic, #cvbtn .ic')){if(!vis(e))continue;const r=e.getBoundingClientRect(),q=e.parentElement.getBoundingClientRect();if(Math.abs((r.top+r.bottom)/2-(q.top+q.bottom)/2)>1)ic.push((e.parentElement.className||'')+' '+e.textContent)}
const av=[];for(const e of document.querySelectorAll('.av')){if(!vis(e))continue;const r=document.createRange();r.selectNodeContents(e);const t=r.getBoundingClientRect(),q=e.getBoundingClientRect();if(Math.abs((t.top+t.bottom)/2-(q.top+q.bottom)/2)>1.5||Math.abs((t.left+t.right)/2-(q.left+q.right)/2)>1.5)av.push(e.textContent+' dy'+((t.top+t.bottom)/2-(q.top+q.bottom)/2).toFixed(1))}
const navOv=document.querySelector('.nav').scrollWidth>innerWidth+1;
return {headClip:[...new Set(hc)],icOff:ic.slice(0,6),avOff:av,navOv,screens:+(document.documentElement.scrollHeight/innerHeight).toFixed(1),xScroll:document.documentElement.scrollWidth>innerWidth,clip:[...new Set(clip)].slice(0,12),clampN:clamp.length,btn:Object.fromEntries(Object.entries(sig).map(([k,v])=>[k,[...v]])),fontN:Object.keys(fonts).length,fonts:Object.entries(fonts).sort((a,b)=>b[1]-a[1]).map(x=>x[0]),colN:Object.keys(cols).length,dur:dur,small:[...new Set(small)].slice(0,14),offR:[...new Set(offR)]}}'''
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    res={}
    for W,H,mob in [(360,740,1),(390,844,1),(768,1024,1),(1024,768,0),(1280,720,0),(1366,768,0),(1440,900,0),(1920,1080,0),(2560,1440,0)]:
      pg=await b.new_page(viewport={'width':W,'height':H},is_mobile=bool(mob),has_touch=bool(mob));errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:120]))
      await pg.goto(URL);await pg.wait_for_timeout(2200)
      for y in range(0,12000,500): await pg.evaluate(f'scrollTo(0,{y})');await pg.wait_for_timeout(40)
      await pg.evaluate("scrollTo({top:0,behavior:'instant'})");await pg.wait_for_timeout(500)
      r=await pg.evaluate(JS);r['errs']=errs
      t=await pg.evaluate('''()=>{const t=[...document.querySelectorAll('.tile')];return t.map(x=>{const tp=x.querySelector('.tp');return tp?(tp.scrollHeight>tp.clientHeight+1||tp.getBoundingClientRect().bottom>x.getBoundingClientRect().bottom-4):false}).filter(Boolean).length}''')
      r['tileTextCut']=t
      hb=await pg.evaluate("(()=>{const h=document.querySelector('.hbar');return h.scrollWidth>h.clientWidth+1})()");r['barOverflow']=hb
      res[f'{W}x{H}']=r;await pg.close()
    await b.close()
    json.dump(res,open('audit-result.json','w'),indent=1)
    fails={k:{x:v[x] for x in ['xScroll','tileTextCut','barOverflow','navOv','errs','headClip','icOff','avOff'] if v[x]} for k,v in res.items()}
    fails={k:v for k,v in fails.items() if v}
    print('PASS' if not fails else 'FAIL',json.dumps(fails,indent=1))
    sys.exit(1 if fails else 0)
asyncio.run(main())
