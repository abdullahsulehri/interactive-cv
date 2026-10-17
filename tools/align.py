"""Icon/label centring check with real fonts (rules A1-A4). Two-tone buttons can give false alarms; confirm visually.
Usage: python tools/align.py [URL]
"""
import asyncio,io,sys,json
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright
SEL='.pa,.btn,.chipb,.hbwa,.nb,.gh'
def ink(img):
  a=np.asarray(img.convert('RGB')).astype(int);h,w,_=a.shape
  if h<4 or w<4:return None
  px=a.reshape(-1,3);vals,cnt=np.unique(px,axis=0,return_counts=True);bg=vals[cnt.argmax()]
  m=(np.abs(a-bg).sum(-1)>200);rows=m.sum(1)
  if rows.max()==0:return None
  top=np.argmax(rows>max(1,rows.max()*.08));base=h-1-np.argmax((rows[::-1]>rows.max()*.3))
  return (top+base)/2
async def run(W,H,mob,url):
  async with async_playwright() as p:
    b=await p.chromium.launch()
    pg=await b.new_page(viewport={'width':W,'height':H},is_mobile=bool(mob),has_touch=bool(mob),device_scale_factor=2)
    await pg.goto(url);await pg.wait_for_timeout(2500)
    els=await pg.query_selector_all(SEL);bad=[];n=0
    for e in els:
      if not await e.is_visible():continue
      box=await e.bounding_box()
      if not box or box['height']<16 or box['width']<16:continue
      await e.scroll_into_view_if_needed();box=await e.bounding_box()
      if box['y']<60 or box['y']+box['height']>H-50:continue
      parts=await e.evaluate("e=>{const q=s=>{const x=e.querySelector(s);if(!x)return null;const r=x.getBoundingClientRect();return r.width?[r.x,r.y,r.width,r.height]:null};return {lb:q('.lb')||(e.classList.contains('pa')?null:[e.getBoundingClientRect().x+8,e.getBoundingClientRect().y,e.getBoundingClientRect().width-16,e.getBoundingClientRect().height]),ic:q('.ic'),t:(e.textContent||'').trim().slice(0,22),cls:e.className}}")
      cy=box['y']+box['height']/2;n+=1
      for k in ('lb','ic'):
        r=parts[k]
        if not r or r[2]<4:continue
        x,y,w,h=r;y0=box['y']+2;h0=box['height']-4
        x0=max(x,box['x']+3);x1=min(x+w,box['x']+box['width']-3)
        if x1-x0<4:continue
        png=await pg.screenshot(clip={'x':x0,'y':y0,'width':x1-x0,'height':h0})
        c=ink(Image.open(io.BytesIO(png)))
        if c is None:continue
        off=(y0+c/2)-cy
        if abs(off)>1.0:bad.append(f"{k}:{parts['t']}:{off:+.1f}")
    await b.close();return n,bad
if __name__=='__main__':
  url=sys.argv[1] if len(sys.argv)>1 else 'https://abdullahsulehri.github.io/interactive-cv/'
  for W,H,mob in [(1440,900,0),(390,844,1)]:
    n,bad=asyncio.run(run(W,H,mob,url));print(W,'checked',n,'misaligned',len(bad),bad[:14])
