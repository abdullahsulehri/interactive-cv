# Rebuilds cv/Abdullah-Sulehri-CV.pdf (2 pages, QR code to the live site).
# Run from repo root: python tools/build_cv.py   (needs reportlab + Liberation Serif fonts)
# CV rules. Checked at the end of every build (exit 1 on failure): exactly 2 pages; no wrapped line left with 1-2 words. Content rules (by hand): no brackets in the summary; course lines carry no years. Needs reportlab + pdfplumber.
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Table,TableStyle,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
F='/usr/share/fonts/truetype/liberation/LiberationSerif'
for n,s in [('S','-Regular'),('S-B','-Bold'),('S-I','-Italic'),('S-BI','-BoldItalic')]:
    pdfmetrics.registerFont(TTFont(n,F+s+'.ttf'))
addMapping('S',0,0,'S');addMapping('S',1,0,'S-B');addMapping('S',0,1,'S-I');addMapping('S',1,1,'S-BI')
BLUE=HexColor('#1F4E79');INK=HexColor('#1A1A1A');GREY=HexColor('#555555')
URL='https://abdullahsulehri.github.io/interactive-cv/?utm_source=cv-pdf'
SHOW='abdullahsulehri.github.io/interactive-cv'
SEP='&nbsp;&nbsp;|&nbsp;&nbsp;';SP2='&nbsp;&nbsp;'
BODY=float(sys.argv[1]) if len(sys.argv)>1 else 10
LEAD=BODY*1.28
def st(**k):
    d=dict(fontName='S',fontSize=BODY,leading=LEAD,textColor=INK,allowWidows=0,allowOrphans=0);d.update(k);return ParagraphStyle('x',**d)
name=st(fontName='S-B',fontSize=21,leading=24,textColor=BLUE,alignment=TA_CENTER)
title=st(fontName='S-B',fontSize=10.5,leading=14,alignment=TA_CENTER)
cont=st(fontSize=9.5,leading=12.5,textColor=GREY,alignment=TA_CENTER)
h=st(fontName='S-B',fontSize=12.5,leading=15,textColor=BLUE,spaceBefore=9,spaceAfter=3)
p=st();job=st(fontName='S-B',spaceBefore=5);date=st(fontName='S-I',textColor=GREY,spaceAfter=1)
bul=st(leftIndent=12,bulletIndent=2)
L=lambda u,t:f'<a href="{u}" color="#555555">{t}</a>'
def B(t):return Paragraph(t,bul,bulletText='•')
def qr():
    w=QrCodeWidget(URL,barLevel='M');w.barBorder=0;b=w.getBounds();s=58.0
    d=Drawing(s,s,transform=[s/(b[2]-b[0]),0,0,s/(b[3]-b[1]),0,0]);d.add(w);return d
qlab=st(fontSize=7.5,leading=9,textColor=GREY,alignment=TA_CENTER)
class QRLink(Table):
    def drawOn(self,c,x,y,_sW=0):
        Table.drawOn(self,c,x,y,_sW);c.linkURL(URL,(x,y,x+self._width,y+self._height),relative=1,thickness=0)
NOPAD=[('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]
qcell=QRLink([[qr()],[Paragraph('<b>Interactive CV</b><br/>scan to open',qlab)]],colWidths=[70])
qcell.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER')]+NOPAD+[('TOPPADDING',(0,1),(0,1),3)]))
mid=[Paragraph('ABDULLAH SULEHRI',name),Paragraph(f'SENIOR MARKETING MANAGER{SEP}B2B GROWTH &amp; AI',title),Spacer(1,2),
 Paragraph('Lahore, Pakistan'+SEP+L('mailto:abdullah@sulehri.com','abdullah@sulehri.com')+SEP+L('tel:+923314074234','+92 331 4074234'),cont),
 Paragraph(L('https://www.linkedin.com/in/abdullahsulehri','linkedin.com/in/abdullahsulehri')+SEP+f'Interactive CV: <a href="{URL}" color="#1F4E79"><u>{SHOW}</u></a>',cont)]
W=612-2*40
hdr=Table([[Spacer(1,1),mid,qcell]],colWidths=[70,W-140,70]);hdr.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE')]+NOPAD))
S=[hdr]
def sec(t):S.append(Paragraph(t,h))
sec('PROFESSIONAL SUMMARY')
S.append(Paragraph('Senior Marketing Manager with nine years in B2B growth, brand, PR and CRM-led marketing across Pakistan and the UAE. Leads a 6-person team at a multi-country HR services group, owning strategy, demand generation, product pricing and the marketing budget. Has built 10+ AI agents and automations that take reporting, checks and content work off the team, with human review on every output. An accounting background brings financial discipline to budgets, pricing and ROI.',p))
sec('CORE MARKETING EXPERTISE')
a=['B2B Marketing Management','Account-Based Marketing (ABM)','Marketing Strategy &amp; GTM Planning','Integrated Marketing Management','Performance Marketing','Email Marketing &amp; Segmentation','Social Media Marketing','SEO &amp; Content Strategy']
b=['Brand &amp; Employer Branding','PR &amp; Communications','CRM &amp; Marketing Automation','AI Agents &amp; Marketing Automation','Marketing Analytics &amp; Reporting','Budget Management &amp; ROI Evaluation','Product Costing &amp; Pricing Strategy','Team Leadership &amp; Stakeholder Management']
cb=st(leftIndent=12,bulletIndent=2,leading=BODY*1.22)
t=Table([[Paragraph(x,cb,bulletText='•'),Paragraph(y,cb,bulletText='•')] for x,y in zip(a,b)],colWidths=[W/2,W/2]);t.setStyle(TableStyle(NOPAD));S.append(t)
sec('TOOLS &amp; PLATFORMS')
for k,v in [('AI &amp; Automation','Claude (incl. Code &amp; Cowork), ChatGPT, Gemini, Copilot, Perplexity, Zapier, Power Automate'),
 ('Growth &amp; Demand','Sales Navigator, Meta, LinkedIn, Google &amp; X Ads, Mailchimp, Zoho Campaigns, Apollo.io, Hootsuite'),
 ('Brand &amp; Content','WordPress, Yoast SEO, SEMrush, Google Trends, Canva, Figma'),
 ('Data &amp; Analytics','Google Analytics, Search Console, Tag Manager, Looker Studio, Power BI, Advanced Excel, Power Query'),
 ('CRM &amp; Operations','Bitrix24, HubSpot, Zoho CRM, Notion, Asana, Trello, Jira, Microsoft 365, Google Workspace')]:
    S.append(Paragraph(f'<b>{k}:</b> {v}',st(spaceAfter=1)))
sec('WORK EXPERIENCE')
def J(role,co,dt,bs):
    S.append(KeepTogether([Paragraph(f'{role}{SEP}{co}',job),Paragraph(dt,date),B(bs[0])]));S.extend(B(x) for x in bs[1:])
J('Senior Marketing Manager','People Perfect',f'Sep 2025 – Present{SP2}(Lahore, Onsite)',[
 'Own end-to-end marketing for a multi-country HR services group: brand, PR, product marketing, content governance, CRM-led growth and B2B demand',
 'Lead a team of 4 direct reports and 2 freelancers across content, design, SEO and digital; manage a ~$10K monthly budget and ROI across campaigns, CRM and content',
 'Led product research and costing for 5 HR consultancy service lines for the company’s upcoming HR services marketplace',
 'Run account-based marketing via LinkedIn Sales Navigator, targeting C-level leaders at UAE enterprises (500+ employees) and owners of large Pakistani FMCG businesses',
 'Recent B2B email campaigns reached a 60% open rate and 5%+ click-through',
 'Run Google, Meta and LinkedIn campaigns, plus Path2Progress, an event and webinar series for senior HR leaders',
 'Final authority on brand and content governance; leading the new company website and office wall branding',
 'Optimize Bitrix24 CRM workflows for lead visibility, lifecycle tracking and sales alignment',
 'Built 10+ human-approved AI agents and automations (Claude, ChatGPT, Zapier, Notion) for reporting and checks'])
J('Marketing Turnaround Project','Fast Food Restaurant, DHA Lahore',f'Jun 2025 – Aug 2025{SP2}(Lahore)',[
 'Reversed a year of falling sales: +25% in month one, then a further +15% in month two (~44% above the starting point)',
 'Improved the burger menu, relaunched consumer campaigns and opened a B2B channel for nearby software houses'])
J('Marketing Manager','Creative Zone Tax &amp; Accounting (UAE)',f'Dec 2022 – May 2025{SP2}(Lahore, Hybrid)',[
 'Led integrated marketing for a UAE tax and accounting firm: brand visibility, demand generation and client acquisition',
 'Turned the new UAE corporate tax (2023) into clear Meta, LinkedIn and X campaigns: 20–40% sustained engagement growth',
 'Owned email marketing and automation; segmentation and A/B testing lifted open rates up to 35%',
 'Directed SEO-led content strategy, growing organic traffic by ~30% across blogs and landing pages',
 'Used SEMrush and Google Trends research to shape go-to-market plans, and reported insights to senior leaders'])
J('Senior Marketing Specialist','Soliton Technologies (Pakistan/US software house)',f'Sep 2021 – Nov 2022{SP2}(Lahore, Onsite)',[
 'Built the marketing function from scratch: website content, blogs, email campaigns and social presence',
 'Led the company rebrand and the launch of a new website',
 'Built the employer brand: employee events, employee of the month, wall branding, merchandise and employee videos',
 'Built university partnerships and represented the company at industry and campus events',
 'Secured PR placements and shared performance insights with SEO, design and development teams via Looker Studio'])
J('Assistant Manager Marketing','Marketing and Advertising Pvt Ltd',f'Jan 2019 – Aug 2021{SP2}(Lahore, Onsite)',[
 'Led integrated digital, influencer and PR campaigns for 20+ brands, incl. Samsung, Unilever, Telenor and Honda',
 'Ran campaigns on X, Instagram, Facebook and LinkedIn with up to 500 influencers each',
 'Averaged ~27M impressions per campaign across social and influencer launches',
 'Coordinated PR agencies, bloggers, publishers and vendors; supervised teams through launches'])
S.append(Paragraph(f'<b>Marketing Executive</b>{SP2}<font name="S-I" color="#555555">Dec 2017 – Dec 2018</font>',st(spaceBefore=3,spaceAfter=1)))
S.append(B('Supported SMS campaigns and content for SME clients; built partnerships with bloggers and online publishers'))
def PJ(t,sub,bs,head=None):
    S.append(KeepTogether(([head] if head else [])+[Paragraph(f'{t}{SP2}<font name="S-I" color="#555555">{sub}</font>',job)]+[B(x) for x in bs]))
PJ('MyndKeep: AI second-brain app','(personal build, 2026)',[
 '<b>Problem:</b> useful reels, posts and notes were scattered across apps, hard to find later and of unclear reliability',
 '<b>Saves anything:</b> links, PDFs, voice notes, screenshots, videos and text; AI categorizes each item automatically',
 '<b>Finds anything:</b> semantic search by meaning, not keywords; 200+ items saved, each with a 5-point trust check',
 '<b>Learns from feedback</b> given by text, voice or screenshot; built with Claude Code, GitHub and Render'],head=Paragraph('SELECTED AI PROJECTS',h))
PJ('Daily website health checker','(People Perfect)',[
 '<b>Problem:</b> broken links and pages on 6 company websites were being found by visitors before the team',
 '<b>Built</b> an automated checker on GitHub Actions that scans 92 pages and 10,000+ links every morning and emails a report; ~300 hidden issues found on the first run'])
S.append(KeepTogether([Paragraph('EDUCATION',h)]+[Paragraph(x,st(spaceAfter=1)) for x in [
 f'<b>ACCA</b> – Member 2016, Fellow 2021{SEP}SKANS School of Accountancy',
 f'<b>Bachelor of Business Administration</b> (2025){SEP}European Global Institute',
 f'<b>Bachelor of Arts – Journalism</b> (2019){SEP}University of the Punjab']]))
# certifications: grouped by skill, one certificate per line, institution first (bold) and linked to its verify page
import json as _j
_C=_j.load(open('content.json'))['certificates']
_F={f['issuer']:f for f in _C['featured']}
_I={i['issuer']:i['items'] for i in _C['issuers']}
_n=sum(len(f['courses'])+len(f.get('also',[])) for f in _C['featured'])+sum(len(v) for v in _I.values())
def L(inst,name,extra,url):
    t=f'<b>{inst}</b> – {name}' + (f' ({extra})' if extra else '')
    return f'<a href="{url}" color="#1A1A1A">{t}</a>' if url else t
G=_F['Google'];A=_F['Anthropic'];M=_F['Meta']
groups=[
 ('Artificial intelligence (AI)',[L('Google','AI Professional Certificate','8 courses',G['url']),
        L('Anthropic','Real-World AI with Claude','3 courses',A['url']),
        L('Anthropic','Claude Code 101','',A['also'][0]['url'])]),
 ('Brand &amp; marketing',[L('Wharton (UPenn)','Introduction to Marketing','',_I['University of Pennsylvania (Wharton)'][0]['url']),
        L('University of London','Brand Management','',_I['University of London'][0]['url']),
        L('University of Illinois','Digital Marketing Revolution','',_I['University of Illinois Urbana-Champaign'][0]['url']),
        L('Meta','Social Media Marketing Certificate','6 courses',M['url'])]),
 ('Advertising',[L('LUMS','Advertising: Print, Outdoor &amp; Digital','',_I['LUMS'][0]['url']),
        L('LinkedIn','Advertising on LinkedIn','',_I['LinkedIn'][0]['url'])]),
 ('SEO &amp; content',[L('UC Davis','Introduction to Google SEO','',_I['UC Davis'][1]['url']),
        L('UC Davis','The Strategy of Content Marketing','',_I['UC Davis'][0]['url'])]),
 ('Project management',[L('Google','Foundations of Project Management','',G['also'][0]['url'])]),
]
gl=st(fontName='S-I',textColor=GREY,spaceBefore=1,spaceAfter=0)
def col(gs):
    out=[]
    for t,items in gs: out+= [Paragraph(t,gl)]+[B(x) for x in items]
    return out
_site=f'<a href="https://abdullahsulehri.github.io/interactive-cv/?utm_source=cv-pdf" color="#1F4E8C">abdullahsulehri.github.io/interactive-cv</a>'
ce=[Paragraph('CERTIFICATIONS',h),Paragraph(f'{_n}+ certificates, all verifiable at {_site}',st(spaceAfter=2))]
_t=Table([[col([groups[0],groups[2],groups[4]]),col([groups[1],groups[3]])]],colWidths=[W*0.5,W*0.5])
_t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),10),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
ce.append(_t)
ce.append(Paragraph('<b>Languages:</b> English, Urdu',st(spaceBefore=3)));S.append(KeepTogether(ce))
doc=BaseDocTemplate('cv/Abdullah-Sulehri-CV.pdf',pagesize=letter,leftMargin=40,rightMargin=40,topMargin=36,bottomMargin=36,
 title='Abdullah Sulehri – CV',author='Abdullah Sulehri',subject='Senior Marketing Manager | B2B Growth & AI',creator='Abdullah Sulehri')
doc.addPageTemplates([PageTemplate('p',[Frame(40,36,W,792-72,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)])]);doc.build(S)
print('pages:',doc.page)
# ---- layout checks (CV rules): exactly 2 pages, and no short orphan lines (a wrapped line left with 1-2 words, like "growth")
def orphans(path):
    import pdfplumber
    out = []
    with pdfplumber.open(path) as pdf:
        for pn, pg in enumerate(pdf.pages, 1):
            rows = {}
            for w in pg.extract_words(keep_blank_chars=False, extra_attrs=['fontname']):
                rows.setdefault(round(w['top'] / 2), []).append(w)
            for k in sorted(rows):
                ws = sorted(rows[k], key=lambda w: w['x0'])
                cols = [[]]
                for w in ws:  # split side-by-side columns (certificates, expertise) at wide gaps
                    if cols[-1] and w['x0'] - cols[-1][-1]['x1'] > 40: cols.append([])
                    cols[-1].append(w)
                for c in cols:
                    t = ' '.join(w['text'] for w in c if w['text'] != '•')
                    label = all('Italic' in w['fontname'] for w in c) or t.isupper() or t.endswith(':')  # group labels, headings
                    if 0 < len(t.split()) <= 2 and not label and c[0]['top'] > 130:  # 1-2 words left alone on a line
                        out.append(f'page {pn}: "{t}"')
    return out
bad = orphans('cv/Abdullah-Sulehri-CV.pdf')
if doc.page != 2 or bad:
    print('CV LAYOUT FAILED:', 'pages=%d' % doc.page if doc.page != 2 else '', *bad, sep='\n - '); sys.exit(1)
print('CV LAYOUT PASS (2 pages, no orphan words)')
