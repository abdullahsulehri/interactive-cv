"""Interaction contract check (rules I1-I5), laptop 1440x900, on the page and inside every panel.
Hovers up to 3 items of each kind/class and fails if one does not answer the cursor the way its kind requires:
  card -> lifts (translate) and is in focus     row -> tint behind it and in focus     mark -> in focus
  any item with its own button -> that button opens (or is a labelled / open control)
Usage: python tools/hovercheck.py http://127.0.0.1:PORT/"""
import asyncio, re, sys, pathlib
from playwright.async_api import async_playwright

root = pathlib.Path(__file__).resolve().parent.parent
ITEMS = re.search(r"const ITEMS = '([^']+)'", (root / 'index.html').read_text()).group(1)
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8000/'

PICK = """(sel) => {
  const seen = {}, out = [];
  document.querySelectorAll('[data-kind]').forEach(el => {
    if (!el.matches(sel) || !el.getClientRects().length) return;
    const pnl = document.getElementById('pnl');
    if (pnl && !pnl.hidden ? !pnl.contains(el) : el.closest('#pnl')) return;
    const key = el.dataset.kind + ':' + [...el.classList].filter(c => !/^(f-|on$|open$|x$|stg$|cur$)/.test(c)).join('.');
    if ((seen[key] = (seen[key] || 0) + 1) > 3) return;
    el.dataset.hc = out.length; out.push(key);
  });
  return out;
}"""
SPOT = """(i) => {
  const el = document.querySelector(`[data-hc="${i}"]`);
  el.scrollIntoView({ block: 'center' });
  const r = el.getBoundingClientRect();
  for (const fy of [0.5, 0.25, 0.75, 0.1, 0.9]) for (const fx of [0.5, 0.2, 0.8, 0.05, 0.95]) {
    const x = r.left + r.width * fx, y = r.top + r.height * fy;
    const hit = document.elementFromPoint(x, y);
    if (hit && hit.closest('[data-kind]') === el && !hit.closest('.pa,a,button:not(.mdb):not([data-kind])')) return [x, y];
  }
  return null;
}"""
STATE = """(i) => {
  const el = document.querySelector(`[data-hc="${i}"]`), cs = getComputedStyle(el), k = el.dataset.kind;
  const own = [...el.querySelectorAll('.pa')].find(p => p.parentElement.closest('[data-kind]') === el && !p.classList.contains('wide'));
  const res = { k, on: el.classList.contains('f-on') || k === 'card' && el.matches('.tile') };
  res.lift = cs.translate !== 'none' && cs.translate !== '0px';
  res.tint = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.boxShadow !== 'none';
  res.pill = !own || own.matches('.f-act,.keep,.on');
  return res;
}"""

async def run():
    fails, n = [], 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        await pg.goto(URL); await pg.wait_for_timeout(2500)
        await pg.add_style_tag(content='html{scroll-behavior:auto!important}')
        if len(sys.argv) > 2 and sys.argv[2] == '--sabotage':  # self-test: with the kind styles switched off, this check must fail
            await pg.add_style_tag(content='.ch [data-kind]:hover{translate:none!important;background-color:transparent!important;box-shadow:none!important}')
        # I5: with a mouse, scrolling alone must never light an item
        await pg.mouse.move(2, 450)
        H = await pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0, H, 450):
            await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(450)
            lit = await pg.evaluate("[...document.querySelectorAll('main [data-kind].f-on')].map(e => e.className.split(' ')[0])")
            if lit: fails.append(f'I5: scrolled to {y}px with the cursor away, items lit anyway: {lit[:3]}'); break
        await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(300)
        tiles = await pg.evaluate("document.querySelectorAll('.tile').length")
        for scope in [-1] + list(range(tiles)):
            if scope >= 0:
                await pg.evaluate(f"document.querySelectorAll('.tile')[{scope}].click()"); await pg.wait_for_timeout(1600)
            await pg.evaluate("document.querySelectorAll('[data-hc]').forEach(e => delete e.dataset.hc)")
            keys = await pg.evaluate(PICK, ITEMS + ',.tile')
            for i, key in enumerate(keys):
                if scope >= 0 and key.startswith('card:tile'): continue
                await pg.mouse.move(2, 450); await pg.wait_for_timeout(250)
                xy = await pg.evaluate(SPOT, i)
                if not xy: continue
                await pg.mouse.move(*xy, steps=3); await pg.wait_for_timeout(650)
                s = await pg.evaluate(STATE, i); n += 1
                bad = [m for m, ok in [('not in focus', s['on']), ('no lift', s['k'] != 'card' or s['lift']),
                       ('no tint', s['k'] != 'row' or s['tint']), ('button stays shut', s['pill'])] if not ok]
                if bad: fails.append(f"{'page' if scope < 0 else 'panel ' + str(scope + 1)} {key}: {', '.join(bad)}")
            if scope >= 0:
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(1000)
        await b.close()
    print(f'{n} items hovered')
    if n < 30: fails.append(f'only {n} items found: kinds are not declared (data-kind missing)')
    for f in fails: print(' -', f)
    print('HOVER PASS (every item answers the cursor by its kind)' if not fails else f'HOVER FAILED ({len(fails)})')
    return not fails

sys.exit(0 if asyncio.run(run()) else 1)
