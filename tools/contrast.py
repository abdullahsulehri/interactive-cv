"""Contrast check in all accent colours (rule K2): every visible text >= 4.5:1 (large text >= 3:1),
in its resting AND highlighted state (pills open, headings lit). Usage: python tools/contrast.py [URL]"""
import asyncio,sys,json
from playwright.async_api import async_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'https://abdullahsulehri.github.io/interactive-cv/'
JS=r"""(state)=>{
const P=s=>{const m=(s.match(/[\d.]+/g)||[]).map(Number);if(!m.length)return [0,0,0,0];if(s.startsWith('color(')){const v=[m[0]*255,m[1]*255,m[2]*255];if(m.length>3)v.push(m[3]);return v}return m};
const lum=([r,g,b])=>{const f=c=>{c/=255;return c<=.03928?c/12.92:((c+.055)/1.055)**2.4};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const mix=(fg,bg)=>{const a=fg.length>3?fg[3]:1;return [0,1,2].map(i=>fg[i]*a+bg[i]*(1-a))};
const bgOf=el=>{let layers=[];for(let e=el;e;e=e.parentElement){const s=getComputedStyle(e);const gi=s.backgroundImage;if(gi&&gi.includes('gradient')&&!gi.includes('url(')&&e!==el.closest('.h1,.thesis,em')){const cols=(gi.match(/(rgba?|color)\([^)]*\)/g)||[]).map(P);if(cols.length)return cols.map(c=>c.slice(0,3))}const c=P(s.backgroundColor);if(c.length<4||c[3]>0){layers.push(c);if(c.length<4||c[3]>=1)break}}let bg=[255,255,255];for(const l of layers.reverse())bg=mix(l,bg);return [bg]};
const out=[];const seen=new Set();
document.querySelectorAll('body *').forEach(el=>{
  if(el.closest('script,style,svg,noscript,input,textarea,select,option,.lgc,[aria-hidden="true"]'))return;
  const t=[...el.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');if(!t)return;
  const r=el.getBoundingClientRect();if(!r.width||!r.height)return;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||+cs.opacity===0)return;
  let op=1;for(let e=el;e;e=e.parentElement)op*=+getComputedStyle(e).opacity;if(op<.05)return;
  const bgs=bgOf(el);const bg=bgs[0];let fg=P(cs.color);
  if(cs.webkitBackgroundClip==='text'||cs.backgroundClip==='text'){const g=cs.backgroundImage.match(/rgba?\([^)]*\)/g);if(g){const pos=cs.backgroundPositionX;const lit=el.closest('.lit,.panel,.xo');fg=P(g[lit?0:1])}}
  fg=mix(fg.length>3?fg:[...fg,1],bg);if(op<1)fg=mix([...fg,op],bg);
  const fs=parseFloat(cs.fontSize),fw=+cs.fontWeight||400,large=fs>=24||(fs>=18.66&&fw>=700);
  const need=large?3:4.5,rt=Math.min(...bgs.map(b=>ratio(fg,b)));
  if(rt<need){const k=t.slice(0,40)+'|'+state;if(!seen.has(k)){seen.add(k);out.push({text:t.slice(0,40),ratio:+rt.toFixed(2),need,cls:(el.className||el.tagName).toString().slice(0,30)})}}
});return out}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1366,'height':768})
        await pg.goto(URL);await pg.wait_for_timeout(1500)
        presets=await pg.evaluate("JSON.parse(document.getElementById('content-data').textContent).settings.accent_presets")
        fails=[]
        for name,col in presets:
            await pg.evaluate(f"document.documentElement.style.setProperty('--accent','{col}')")
            for state,setup in [('rest',"document.querySelectorAll('.f-on,.f-act,.lit').forEach(e=>e.classList.remove('f-on','f-act','lit'))"),
                                ('focus',"document.querySelectorAll('.pa').forEach(e=>e.classList.add('f-act'));document.querySelectorAll('.h1,.thesis').forEach(e=>e.classList.add('lit'))")]:
                await pg.evaluate("document.documentElement.classList.add('no-motion');document.querySelectorAll('*').forEach(e=>e.style.transition='none')")
                await pg.evaluate(setup);await pg.wait_for_timeout(150)
                for f in await pg.evaluate(JS,state):fails.append(dict(accent=name,state=state,**f))
        await b.close()
    for f in fails[:40]:print(f"{f['accent']:<10} {f['state']:<5} {f['ratio']:>4}/{f['need']}  {f['cls']:<28} {f['text']}")
    print(f'\n{len(fails)} contrast failures' if fails else 'CONTRAST PASS (6 accents, rest + highlighted)');sys.exit(1 if fails else 0)
asyncio.run(main())
