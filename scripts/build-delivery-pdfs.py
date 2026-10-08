from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
FONT = Path('/System/Library/Fonts/Supplemental')
for name, file in [('Arial','Arial.ttf'),('ArialBold','Arial Bold.ttf'),('ArialItalic','Arial Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='ArialItalic',boldItalic='ArialBold')
NAVY=HexColor('#15213a'); BLUE=HexColor('#3058e9'); GRAY=HexColor('#566174'); PALE=HexColor('#edf1ff')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyU',fontName='Arial',fontSize=10.5,leading=15.4,textColor=NAVY,spaceAfter=8,allowWidows=0,allowOrphans=0))
styles.add(ParagraphStyle(name='H2U',fontName='ArialBold',fontSize=15.2,leading=19,textColor=NAVY,spaceBefore=14,spaceAfter=9,keepWithNext=True))
styles.add(ParagraphStyle(name='H3U',fontName='ArialBold',fontSize=11.7,leading=16,textColor=BLUE,spaceBefore=9,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='CaptionU',fontName='Arial',fontSize=9.2,leading=13.5,textColor=GRAY,spaceAfter=8))
styles.add(ParagraphStyle(name='TitleU',fontName='ArialBold',fontSize=32,leading=38,textColor=NAVY,spaceAfter=12))
styles.add(ParagraphStyle(name='LeadU',fontName='Arial',fontSize=13,leading=18,textColor=GRAY,spaceAfter=16))
styles.add(ParagraphStyle(name='SmallU',fontName='Arial',fontSize=9.4,leading=13.8,textColor=NAVY,spaceAfter=5))
styles.add(ParagraphStyle(name='ListU',fontName='Arial',fontSize=10.5,leading=15.4,textColor=NAVY,leftIndent=14,firstLineIndent=-12,spaceAfter=6))

class NumberedCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        canvas.Canvas.__init__(self,*args,**kwargs); self.saved=[]
    def showPage(self):
        self.saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total=len(self.saved)
        for state in self.saved:
            self.__dict__.update(state)
            self.setStrokeColor(HexColor('#d9dfeb')); self.setLineWidth(.5); self.line(43,43,552,43)
            self.setFont('Arial',8); self.setFillColor(GRAY)
            self.drawString(43,29,'UMBRAL / WEEK 9 / OPERATOR / FICTIONAL DEMONSTRATION')
            self.drawRightString(552,29,f'{self._pageNumber} / {total}')
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def header(c,doc):
    c.saveState(); c.setFillColor(BLUE); c.rect(0,828,595,14,fill=1,stroke=0)
    c.setFont('ArialBold',8.5); c.setFillColor(GRAY); c.drawString(43,807,doc.report_label)
    c.drawRightString(552,807,'7 OCTOBER 2026'); c.restoreState()

def markup(s):
    s=s.replace('—','-').replace('–','-').replace('->',' > ')
    s=escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'\1',s)
    s=re.sub(r'(https://[^\s]+)', lambda m: '<link href="'+m.group(1).rstrip('.')+'" color="#3058e9">'+m.group(1).rstrip('.')+'</link>'+('.' if m.group(1).endswith('.') else ''),s)
    return s

def md(path,skip_title=True):
    out=[]; para=[]
    def flush():
        if para: out.append(Paragraph(markup(' '.join(para)),styles['BodyU']));para.clear()
    for line in path.read_text().splitlines():
        t=line.strip()
        if t.startswith('# '):
            flush()
            if not skip_title:out.append(Paragraph(markup(t[2:]),styles['H2U']))
        elif t.startswith('## '):flush();out.append(Paragraph(markup(t[3:]),styles['H2U']))
        elif t.startswith('### '):flush();out.append(Paragraph(markup(t[4:]),styles['H3U']))
        elif not t:flush()
        elif re.match(r'^\d+\. ',t):flush();out.append(Paragraph(markup(t),styles['ListU']))
        elif t.startswith('- '):flush();out.append(Paragraph('- '+markup(t[2:]),styles['ListU']))
        else:para.append(t)
    flush();return out

def image_card(path,max_w=245,max_h=465):
    iw,ih=ImageReader(str(path)).getSize(); f=min(max_w/iw,max_h/ih)
    return Image(str(path),width=iw*f,height=ih*f,hAlign='LEFT')

def callout(text):
    t=Table([[Paragraph(markup(text),styles['SmallU'])]],colWidths=[509])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.6,HexColor('#d6def8')),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return t

def intro(title,subtitle,note):
    return [Paragraph('UMBRAL',styles['TitleU']),Paragraph(subtitle,styles['LeadU']),callout(note),Spacer(1,13)]

def build(filename,label,story):
    d=SimpleDocTemplate(str(OUT/filename),pagesize=(595,842),rightMargin=43,leftMargin=43,topMargin=59,bottomMargin=59,title=label,author='Rodrigo Peña León',subject='Week 9 - OPERATOR - Umbral',pageCompression=1)
    d.report_label=label.upper();d.build(story,onFirstPage=header,onLaterPages=header,canvasmaker=NumberedCanvas)

packet=intro('UMBRAL','Business Bending Packet / First-Proof / OPERATOR','Functional educational demonstration. Team Blueprint draft status preserved. Live LLM activation and original recording evidence remain outstanding.')+md(ROOT/'docs/PACKET.md')
packet += [PageBreak(),Paragraph('11. Actual interface and workflow',styles['H2U']),Paragraph('Capture from the real local build. The 446-pixel viewport is the integrated browser default. Fictional states shown here are produced by the walkthrough; they are not pilot results.',styles['BodyU'])]
left=image_card(ROOT/'evidence/build-preview.jpg',max_w=238,max_h=470)
right=[Paragraph('A usable first rung needs an operating process',styles['H3U']),Paragraph('Named reviewer and deadlines precede the sample. The three fixture cases are labeled fictional. The ten-minute card is a proposed pilot threshold.',styles['BodyU']),Paragraph('Privacy gates',styles['H3U']),Paragraph('Invitation > explanation > human review > private candidate result > accuracy confirmation > recipient permission.',styles['BodyU']),Paragraph('Correction or substantive new review invalidates earlier approval and permission. An incomplete observation stays private and may be retried.',styles['BodyU']),Paragraph('Scope of proof',styles['H3U']),Paragraph('One fictional task with version, reviewer, observed revision, assistance disclosure and a named recipient. No universal score or promise of employment.',styles['BodyU'])]
t=Table([[left,right]],colWidths=[250,259]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),12)]));packet+=[t]
packet += [PageBreak(),Paragraph('12. Implementation specification',styles['H2U'])]+md(ROOT/'docs/BUILD_PROMPT.md')
packet += [Paragraph('13. Delivery provenance',styles['H2U']),Paragraph('The Packet was first committed as c3a13ed before product-source code. Version 1 was published successfully from 91adef9722b03b9f083eeb818482e2a2ecc692b3. The managed source preserves meaningful commits. Deployment status and subsequent refinements are recorded in docs/DEPLOYMENT_LOG.md. The supplied Blueprint is preserved outside the app repository.',styles['BodyU']),Paragraph('Sources: Team 2 Blueprint supplied by Rodrigo; Rodrigo\'s final individual Brain brief; actual app and Git history. Operating references: Riipen Educators (https://www.riipen.com/educators), Forage (https://www.theforage.com/) and official Gemini text-generation documentation (https://ai.google.dev/gemini-api/docs/text-generation). These references do not validate the proposed pilot.',styles['CaptionU'])]
build('PACKET_Rodrigo_Pena_WEEK9.pdf','Business Bending Packet',packet)

persona=intro('UMBRAL','Synthetic Persona Report / Candidate control','Generated roleplay and actual fictional browser observations. No participant interview, real human assessment, employer decision or pilot result.')+md(ROOT/'docs/PERSONA_REPORT.md')
persona += [PageBreak(),Paragraph('8. Interface evidence',styles['H2U']),Paragraph('Actual app captures. The correction request kept the case private; the AI helper explicitly reported missing configuration. Full captures and the visible fictional JSON are retained locally with the source.',styles['BodyU'])]
persona += [callout('Observed UI: Corrección solicitada. El registro sigue privado hasta resolverla.'),Spacer(1,12)]
rows=[
 [Paragraph('<b>Action performed with fictional data</b>',styles['SmallU']),Paragraph('<b>Visible result</b>',styles['SmallU'])],
 [Paragraph('Request a correction to observation wording.',styles['SmallU']),Paragraph('Approval/share path removed; correction pending; old recipient revoked.',styles['SmallU'])],
 [Paragraph('Save the amended simulated review.',styles['SmallU']),Paragraph('Resultado privado; unchecked accuracy confirmation required again.',styles['SmallU'])],
 [Paragraph('Revoke a recipient permission.',styles['SmallU']),Paragraph('Revocado; recipient export controls removed. Previously downloaded copies cannot be recalled.',styles['SmallU'])],
 [Paragraph('Open scope wording assistance without provider secret.',styles['SmallU']),Paragraph('La asistencia con IA todavía no está configurada. Puedes usar la plantilla revisada.',styles['SmallU'])],
 [Paragraph('Prepare authorized JSON.',styles['SmallU']),Paragraph('Visible task, reviewer, observed revision and exact recipient. Selection fallback worked; download completion unverified.',styles['SmallU'])]
]
t=Table(rows,colWidths=[220,289]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PALE),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f7f9fc')]),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d9dfeb')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7)]));persona += [t,Spacer(1,12),Paragraph('Capture provenance: evidence/correction-private.jpg, evidence/candidate-private.jpg, evidence/ai-unavailable.jpg and evidence/proof-preview.jpg. Full original images are kept with the local build; these text excerpts report observed labels without reducing long phone captures to unreadable figures.',styles['CaptionU'])]
persona += [Paragraph('Reproducibility and limits',styles['H3U']),Paragraph('The persona prompt, interpretation, browser observations and changes are preserved in docs/PERSONA_PROMPT.md, docs/PERSONA_REPORT.md and docs/TEST_LOG.md. Download completion and OS PDF saving remain unverified. The synthetic scenario supplies a test case, not evidence of user prevalence, institutional adoption or ability.',styles['BodyU'])]
build('PERSONA_Rodrigo_Pena_WEEK9.pdf','Synthetic Persona Report',persona)
print('Created Packet and Synthetic Persona PDFs.')
