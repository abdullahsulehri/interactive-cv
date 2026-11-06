# Rebuilds cv/Abdullah-Sulehri-CV.pdf (2 pages, QR code to the live site).
# Run from repo root: python tools/build_cv.py   (needs reportlab + Liberation Serif fonts)
# After editing text: rebuild, check it is still 2 pages, and that the QR still scans.
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
qcell=QRLink([[qr()],[Paragraph('<b>Interactive CV</b><br/>scan or click',qlab)]],colWidths=[70])
qcell.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER')]+NOPAD+[('TOPPADDING',(0,1),(0,1),3)]))
mid=[Paragraph('ABDULLAH SULEHRI',name),Paragraph(f'SENIOR MARKETING MANAGER{SEP}B2B GROWTH &amp; AI',title),Spacer(1,2),
 Paragraph('Lahore, Pakistan'+SEP+L('mailto:abdullah@sulehri.com','abdullah@sulehri.com')+SEP+L('tel:+923314074234','+92 331 4074234'),cont),
 Paragraph(L('https://www.linkedin.com/in/abdullahsulehri','linkedin.com/in/abdullahsulehri')+SEP+f'Portfolio: <a href="{URL}" color="#1F4E79"><u>{SHOW}</u></a>',cont)]
W=612-2*40
hdr=Table([[Spacer(1,1),mid,qcell]],colWidths=[70,W-140,70]);hdr.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE')]+NOPAD))
S=[hdr]
def sec(t):S.append(Paragraph(t,h))
sec('PROFESSIONAL SUMMARY')
S.append(Paragraph('Senior Marketing Manager with nine years in B2B growth, brand, PR and CRM-led marketing across Pakistan and the UAE. Leads a 6-person marketing function (4 direct reports, 2 freelancers) for a first-of-its-kind HR services marketplace, owning strategy, demand generation, product pricing and a ~$10K monthly budget. Builds AI agents and automations (10+ live) that take reporting, checks and content work off the team, with human review on every output. ACCA Fellow, bringing financial discipline to budgeting, pricing and ROI.',p))
sec('CORE MARKETING EXPERTISE')
a=['B2B Marketing Management','Account-Based Marketing (ABM)','Marketing Strategy &amp; GTM Planning','Integrated Marketing Management','Performance Marketing','Email Marketing &amp; Segmentation','Social Media Marketing','SEO &amp; Content Strategy']
b=['Brand &amp; Employer Branding','PR &amp; Communications','CRM &amp; Marketing Automation','AI Agents &amp; Marketing Automation','Marketing Analytics &amp; Reporting','Budget Management &amp; ROI Evaluation','Product Costing &amp; Pricing Strategy','Team Leadership &amp; Stakeholder Management']
cb=st(leftIndent=12,bulletIndent=2,leading=BODY*1.22)
t=Table([[Paragraph(x,cb,bulletText='•'),Paragraph(y,cb,bulletText='•')] for x,y in zip(a,b)],colWidths=[W/2,W/2]);t.setStyle(TableStyle(NOPAD));S.append(t)
sec('TOOLS &amp; PLATFORMS')
for k,v in [('AI &amp; Automation','Claude (incl. Claude Code, Cowork, Design), ChatGPT, Gemini, Microsoft Copilot, Perplexity, Zapier, Power Automate'),
 ('Growth &amp; Demand','LinkedIn Sales Navigator, Meta Ads, LinkedIn Ads, Google Ads, X Ads, Mailchimp, Zoho Campaigns, Apollo.io, Hootsuite'),
 ('Brand &amp; Content','WordPress, Yoast SEO, SEMrush, Google Trends, Canva, Figma'),
 ('Data &amp; Analytics','Google Analytics, Search Console, Tag Manager, Looker Studio, Power BI, Advanced Excel, Power Query'),
 ('CRM &amp; Operations','Bitrix24, HubSpot, Zoho CRM, Microsoft Bookings, Notion, Asana, Trello, Jira, Microsoft Office, Google Workspace')]:
    S.append(Paragraph(f'<b>{k}:</b> {v}',st(spaceAfter=1)))
sec('WORK EXPERIENCE')
def J(role,co,dt,bs):
    S.append(KeepTogether([Paragraph(f'{role}{SEP}{co}',job),Paragraph(dt,date),B(bs[0])]));S.extend(B(x) for x in bs[1:])
J('Senior Marketing Manager','People Perfect',f'Sep 2025 – Present{SP2}(Lahore, Onsite)',[
 'Own end-to-end marketing strategy for a first-of-its-kind HR services marketplace: brand, PR, product marketing, content governance, CRM-led growth and B2B demand',
 'Lead a team of 4 direct reports and 2 freelancers across content, design, SEO and digital; manage a ~$10K monthly budget and ROI across campaigns, CRM and content',
 'Led product research and costing for 5 HR consultancy service lines, with pricing now live on the marketplace',
 'Run account-based marketing via LinkedIn Sales Navigator, targeting C-level leaders at UAE enterprises (500+ employees) and owners of large Pakistani FMCG businesses',
 'Recent B2B email campaigns reached a 60% open rate and 5%+ click-through',
 'Run Google, Meta and LinkedIn campaigns, plus Path2Progress, an event and webinar series for senior HR leaders',
 'Final authority on brand and content governance; leading the new company website and office wall branding',
 'Optimize Bitrix24 CRM workflows for lead visibility, lifecycle tracking and sales alignment',
 'Built 10+ AI agents and automations (Claude, ChatGPT, Zapier, Notion) for reporting, website checks and content review, each human-approved'])
J('Marketing Turnaround Project','Fast Food Restaurant, DHA Lahore',f'Jun 2025 – Aug 2025{SP2}(Lahore)',[
 'Reversed a year of falling sales: +25% in month one, then a further +15% in month two (~44% above the starting point)',
 'Strengthened the burger menu, relaunched consumer campaigns, and opened a new B2B channel with offers for teams at nearby software houses'])
J('Marketing Manager','Creative Zone Tax &amp; Accounting (UAE)',f'Dec 2022 – May 2025{SP2}(Lahore, Hybrid)',[
 'Led integrated marketing for a UAE tax and accounting firm: brand visibility, demand generation and client acquisition',
 'Turned the new UAE corporate tax (2023) into clear Meta, LinkedIn and X campaigns, delivering 20–40% sustained engagement growth',
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
 'Delivered integrated digital, influencer and PR campaigns for 20+ brands, including Samsung, Unilever, Telenor, Honda and National Foods',
 'Ran campaigns across X, Instagram, Facebook and LinkedIn with up to 500 influencers, averaging ~27M impressions per campaign',
 'Coordinated PR agencies, bloggers, publishers and vendors, and supervised cross-functional teams during high-pressure launches'])
S.append(Paragraph(f'<b>Marketing Executive</b>{SP2}<font name="S-I" color="#555555">Dec 2017 – Dec 2018</font>',st(spaceBefore=3,spaceAfter=1)))
S.append(B('Supported SMS campaigns and content for SME clients; built partnerships with bloggers and online publishers'))
def PJ(t,sub,bs,head=None):
    S.append(KeepTogether(([head] if head else [])+[Paragraph(f'{t}{SP2}<font name="S-I" color="#555555">{sub}</font>',job)]+[B(x) for x in bs]))
PJ('MyndKeep: AI second-brain app','(personal build, 2026)',[
 '<b>Problem:</b> useful reels, posts and notes were scattered across apps, hard to find later and of unclear reliability',
 '<b>Built</b> an Android app (shared as an APK with friends) that captures reels, screenshots, voice notes and docs; Gemini sorts, summarizes and runs a 5-point trust check on each item; 200+ items saved so far',
 '<b>Owned every product call:</b> review-first ingestion, scope cuts, categories and UI; built with Claude Code, GitHub and Render'],head=Paragraph('SELECTED AI PROJECTS',h))
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
 ('AI',[L('Google','AI Professional Certificate','8 courses, 2026',G['url']),
        L('Anthropic','Real-World AI with Claude','3 courses, 2026',A['url']),
        L('Anthropic','Claude Code 101','2026',A['also'][0]['url'])]),
 ('Brand &amp; marketing',[L('Wharton (UPenn)','Introduction to Marketing','2022',_I['University of Pennsylvania (Wharton)'][0]['url']),
        L('University of London','Brand Management','2023',_I['University of London'][0]['url']),
        L('University of Illinois','The Digital Marketing Revolution','2023',_I['University of Illinois Urbana-Champaign'][0]['url']),
        L('Meta','Social Media Marketing Certificate','6 courses, 2026',M['url'])]),
 ('Advertising',[L('LUMS','Advertising: Print, Outdoor &amp; Digital','2023',_I['LUMS'][0]['url']),
        L('LinkedIn','Advertising on LinkedIn','2023',_I['LinkedIn'][0]['url'])]),
 ('SEO &amp; content',[L('UC Davis','Introduction to Google SEO','2022',_I['UC Davis'][1]['url']),
        L('UC Davis','The Strategy of Content Marketing','2023',_I['UC Davis'][0]['url'])]),
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
