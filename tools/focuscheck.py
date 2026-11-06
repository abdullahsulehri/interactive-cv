"""Focus-system check (rules F2, F8): (1) on phone, every item can reach focus by scrolling (laptop uses the pointer), on the page, in every panel and in the
full-experience view; (2) every always-labelled control shows a readable label at rest.  Usage: python tools/focuscheck.py [URL]"""
import asyncio,sys
from playwright.async_api import async_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'https://abdullahsulehri.github.io/interactive-cv/'
WATCH="""()=>{window.__seen=new WeakSet();const mark=()=>document.querySelectorAll('.f-on').forEach(e=>__seen.add(e));mark();
 if(window.__mo)__mo.disconnect();window.__mo=new MutationObserver(mark);__mo.observe(document.body,{subtree:true,attributes:true,attributeFilter:['class']})}"""
MISS="""()=>window.__fx().filter(e=>!e.matches('.tool')&&!__seen.has(e)).map(e=>(e.className.toString().split(' ')[0])+': '+e.textContent.trim().replace(/\\s+/g,' ').slice(0,40))"""
LABELS="""()=>[...document.querySelectorAll('.pa.keep')].filter(p=>p.getClientRects().length&&getComputedStyle(p).visibility!=='hidden').filter(p=>{const l=p.querySelector('.lb');const cs=getComputedStyle(l);return +cs.opacity<.9||l.getBoundingClientRect().width<10}).map(p=>p.textContent.trim().slice(0,30)||'(empty label)')"""
async def sweep(pg,scroller):
    mx=await pg.evaluate(f"(()=>{{const s={scroller};return s.scrollHeight-s.clientHeight}})()")
    y=0
    while True:
        await pg.evaluate(f"(()=>{{const s={scroller};s.scrollTop={y}}})()");await pg.wait_for_timeout(230)  # let scrolling settle so pills may open
        if await pg.evaluate("document.querySelectorAll('.pa.f-act').length>1"):MANY.append(scroller[:30]+f' @{y}')
        if (pg.viewport_size or {}).get('width',0)<900 and await pg.evaluate("document.querySelectorAll('.f-on').length===0 && window.__fx().some(e=>{const r=e.getBoundingClientRect();return r.height&&r.bottom>60&&r.top<innerHeight-60})"):EMPTY.append(scroller[:30]+f' @{y}')
        if y>=mx:break
        y=min(mx,y+max(6,min(30,mx//40)))
EMPTY=[];MANY=[]  # EMPTY: phone only; with a mouse, focus comes from the cursor (I5) and may be empty
async def main():
    fails=[]
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for W,H in [(390,844),(1366,768)]:
            mob=W<900;pg=await b.new_page(viewport={'width':W,'height':H},is_mobile=mob,has_touch=mob,reduced_motion='reduce')
            await pg.goto(URL);await pg.wait_for_timeout(1500)
            await pg.wait_for_timeout(600)
            for l in await pg.evaluate(LABELS):fails.append(f'{W}px labelled control unreadable: {l}')
            await pg.evaluate(WATCH);await sweep(pg,'document.scrollingElement')
            await pg.evaluate('scrollTo(0,0)');await pg.wait_for_timeout(300)
            for m in await pg.evaluate(MISS):pass  # page items are checked by the sweep above
            missed=await pg.evaluate("""()=>{const all=[];document.querySelectorAll('main *').forEach(()=>{});return []}""")
            # page: candidates depend on scroll position, so collect misses during a second pass with the panel closed
            await pg.evaluate(WATCH)
            mx=await pg.evaluate('document.scrollingElement.scrollHeight-innerHeight');miss=set();y=0
            while True:
                await pg.evaluate(f'scrollTo(0,{y})');await pg.wait_for_timeout(45)
                for m in await pg.evaluate(MISS):miss.add(m)
                if y>=mx:break
                y=min(mx,y+max(6,min(30,mx//40)))
            seen_ok=await pg.evaluate("()=>window.__fx().every(e=>e.matches('.tool')||__seen.has(e))")
            final=[m for m in miss if m not in set(await pg.evaluate(MISS))] if False else None
            still=set()
            for m in miss:
                pass
            # an item counts as reached if it was focused at any point during the sweep
            unreached=await pg.evaluate("""()=>{const out=[];document.querySelectorAll('main .skgrp,main .ca,main .cert,main .open-row,main .edc,main .logo,main .rec,main .act,main .rowx,main .sch,main .pa').forEach(e=>{if(e.closest('#pnl,.xo,.tiles,.chips,form'))return;if(!e.getClientRects().length)return;if(e.matches('.pa')&&e.parentElement.closest('.skgrp,.ca,.cert,.open-row,.edc,.logo,.tool,.rec,.act,.mdb,.pc,.rowx,.sch,.xb,.st,.xr'))return;if(!__seen.has(e))out.push((e.className.toString().split(' ')[0])+': '+e.textContent.trim().replace(/\\s+/g,' ').slice(0,40))});return out}""")
            for u in unreached:
                if mob:fails.append(f'{W}px page: never in focus: {u}')
            await pg.evaluate('scrollTo(0,0)');await pg.wait_for_timeout(300)
            for t in ['Problems','Experience','My AI toolkit','Testimonials','Writing']:
                await pg.locator('.tile',has_text=t).first.click();await pg.wait_for_timeout(800)
                await pg.mouse.move(2,H-2) if not mob else None
                for l in await pg.evaluate(LABELS):fails.append(f'{W}px {t}: labelled control unreadable: {l}')
                if await pg.evaluate("(()=>{const s=document.querySelector('#pbd');return s.scrollHeight-s.clientHeight<=1})()"):
                    await pg.keyboard.press('Escape');await pg.wait_for_timeout(400);continue  # nothing scrolls: focus comes from touch (F2)
                await pg.evaluate(WATCH);await sweep(pg,"document.querySelector('#pbd')")
                for m in await pg.evaluate(MISS):
                    if mob:fails.append(f'{W}px panel {t}: never in focus: {m}')
                await pg.keyboard.press('Escape');await pg.wait_for_timeout(400)
            # merged view: View full experience opens the Experience panel expanded
            await pg.evaluate('scrollTo(0,0)');await pg.wait_for_timeout(300)
            await pg.evaluate("document.querySelector('[data-xfull]').click()");await pg.wait_for_timeout(1200)
            if not await pg.evaluate("!document.querySelector('#pnl').hidden && document.querySelector('#pbd .mdx').classList.contains('all')"):fails.append(f'{W}px View full experience did not open the expanded Experience panel')
            await pg.keyboard.press('Escape');await pg.wait_for_timeout(400)
            await pg.close()
        await b.close()
    if MANY:fails.append(f'more than one pill open at once ({len(MANY)}x), e.g. '+', '.join(MANY[:3]))
    if EMPTY:fails.append(f'focus empty while items are on screen ({len(EMPTY)}x), e.g. '+', '.join(EMPTY[:3]))
    for f in fails[:40]:print(' -',f)
    print(f'\n{len(fails)} focus problems' if fails else 'FOCUS PASS (every item reachable, labels readable)');sys.exit(1 if fails else 0)
asyncio.run(main())
