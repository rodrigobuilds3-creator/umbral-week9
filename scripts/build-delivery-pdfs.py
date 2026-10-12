from pathlib import Path
from xml.sax.saxutils import escape
import re
import sys
import json
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
styles.add(ParagraphStyle(name='CodeU',fontName='Arial',fontSize=8,leading=11,textColor=NAVY,spaceAfter=1,wordWrap='CJK'))
styles.add(ParagraphStyle(name='RawU',fontName='Arial',fontSize=9.1,leading=13,textColor=NAVY,spaceAfter=7,wordWrap='CJK'))
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
    c.drawRightString(552,807,'11 OCTOBER 2026'); c.restoreState()

def markup(s):
    s=s.replace('—','-').replace('–','-').replace('->',' > ')
    s=escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'\1',s)
    s=re.sub(r'(https://[^\s]+)', lambda m: '<link href="'+m.group(1).rstrip('.')+'" color="#3058e9">'+m.group(1).rstrip('.')+'</link>'+('.' if m.group(1).endswith('.') else ''),s)
    return s

def md(path,skip_title=True):
    out=[]; para=[]; code=[]; in_code=False; table=[]
    def flush():
        if para: out.append(Paragraph(markup(' '.join(para)),styles['BodyU']));para.clear()
    def flush_table():
        if not table:return
        rows=[]
        for row in table:
            vals=[x.strip() for x in row.strip('|').split('|')]
            if all(re.fullmatch(r'[:\- ]+',x or '-') for x in vals):continue
            rows.append([Paragraph(markup(x),styles['SmallU']) for x in vals])
        if rows:
            n=len(rows[0]); widths=[509/n]*n
            t=Table(rows,colWidths=widths,repeatRows=1)
            t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,-1),.3,HexColor('#d9dfeb')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));out.append(t);out.append(Spacer(1,10))
        table.clear()
    for line in path.read_text().splitlines():
        t=line.strip()
        if t.startswith('```'):
            flush();flush_table()
            if in_code:
                for c in code:out.append(Paragraph(escape(c).replace(' ','&#160;'),styles['CodeU']))
                code.clear();out.append(Spacer(1,10))
            in_code=not in_code;continue
        if in_code:code.append(line);continue
        if t.startswith('|'):flush();table.append(t);continue
        flush_table()
        if t.startswith('# '):
            flush()
            if not skip_title:out.append(Paragraph(markup(t[2:]),styles['H2U']))
        elif t.startswith('## '):flush();out.append(Paragraph(markup(t[3:]),styles['H2U']))
        elif t.startswith('### '):flush();out.append(Paragraph(markup(t[4:]),styles['H3U']))
        elif not t:flush()
        elif re.match(r'^\d+\. ',t):flush();out.append(Paragraph(markup(t),styles['ListU']))
        elif t.startswith('- '):flush();out.append(Paragraph('- '+markup(t[2:]),styles['ListU']))
        else:para.append(t)
    flush();flush_table();return out

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
    d=SimpleDocTemplate(str(OUT/filename),pagesize=(595,842),rightMargin=43,leftMargin=43,topMargin=59,bottomMargin=59,title=label,author='Rodrigo Peña de León',subject='Week 9 - OPERATOR - Umbral',pageCompression=1)
    d.report_label=label.upper();d.build(story,onFirstPage=header,onLaterPages=header,canvasmaker=NumberedCanvas)

from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon

def workflow_diagram():
    d=Drawing(509,535)
    def box(x,y,w,h,lines):
        d.add(Rect(x,y,w,h,rx=6,ry=6,fillColor=PALE,strokeColor=HexColor('#bac8e7'),strokeWidth=.7))
        for i,t in enumerate(lines):d.add(String(x+w/2,y+h/2+(len(lines)-1)*6-i*12,t,textAnchor='middle',fontName='Arial',fontSize=9,fillColor=NAVY))
    def arrow(x1,y1,x2,y2,label=''):
        d.add(Line(x1,y1,x2,y2,strokeColor=BLUE,strokeWidth=1))
        import math
        a=math.atan2(y2-y1,x2-x1);l=5
        d.add(Polygon([x2,y2,x2-l*math.cos(a-.5),y2-l*math.sin(a-.5),x2-l*math.cos(a+.5),y2-l*math.sin(a+.5)],fillColor=BLUE,strokeColor=BLUE))
        if label:d.add(String((x1+x2)/2+4,(y1+y2)/2+4,label,fontName='Arial',fontSize=8,fillColor=GRAY))
    labels=[['Operador: tarea ficticia,','revisor y plazos'],['Candidato: explicación','y asistencia declarada'],['Revisor: criterios y','condición que cambia'],['Resultado privado','para el candidato'],['¿Necesita corrección?'],['Confirmar exactitud:','el registro sigue privado'],['¿Permiso opcional','para un destinatario?']]
    for i,l in enumerate(labels):box(35,480-i*64,280,45,l)
    for i in range(6):arrow(175,480-i*64,175,461-i*64,'No' if i==4 else '')
    box(355,205,145,70,['Solicitar corrección:','revocar permisos','y volver al revisor'])
    arrow(315,246,355,246,'Sí');d.add(Line(427,275,427,374,strokeColor=BLUE));arrow(427,374,315,374)
    box(5,10,135,56,['Terminar con','resultado privado']);arrow(85,96,72,66,'No')
    box(178,10,155,56,['Nombre, finalidad,','plazo y consentimiento']);arrow(245,96,255,66,'Sí')
    box(362,10,140,56,['JSON / impresión local','Revocar bloquea','nuevas copias']);arrow(333,38,362,38)
    return d

def lanes_diagram():
    d=Drawing(509,570);xs=[55,190,320,454]
    for x,t in zip(xs,['Operador','Candidato','Revisor humano','Flujo local']):
        d.add(Rect(x-53,529,106,34,rx=5,ry=5,fillColor=PALE,strokeColor=HexColor('#bac8e7')))
        d.add(String(x,542,t,textAnchor='middle',fontName='ArialBold',fontSize=9,fillColor=NAVY))
        d.add(Line(x,523,x,20,strokeColor=HexColor('#bac8e7'),strokeWidth=.7))
    events=[(0,3,'Tarea ficticia, responsable y plazos'),(3,1,'Invitación y rúbrica'),(1,2,'Explicación y asistencia declarada'),(2,3,'Criterios, cambio observado y minutos'),(3,1,'Resultado privado primero'),(1,3,'Si corrige: revocar permisos'),(3,2,'Resolver corrección y revisar de nuevo'),(1,3,'Confirmar exactitud: aún privado'),(1,3,'Opcional: permiso por destinatario'),(3,1,'Copia local; sin envío automático')]
    for i,(a,b,t) in enumerate(events):
        y=490-i*48;x1=xs[a];x2=xs[b]
        d.add(Line(x1,y,x2,y,strokeColor=BLUE,strokeWidth=1))
        sign=1 if x2>x1 else -1
        d.add(Polygon([x2,y,x2-6*sign,y+3,x2-6*sign,y-3],fillColor=BLUE,strokeColor=BLUE))
        d.add(String((x1+x2)/2,y+9,t,textAnchor='middle',fontName='Arial',fontSize=8.3,fillColor=NAVY))
    return d

packet=intro('UMBRAL','Business Bending Packet / First-Proof / OPERATOR','Functional fictional demonstration with real Gemini drafting. Packet core preceded code; design/architecture additions are dated after implementation. Original human recordings and final team agreement remain outstanding.')+md(ROOT/'docs/PACKET.md')
packet += [PageBreak(),Paragraph('11. Actual interface and workflow',styles['H2U']),Paragraph('Capture from the real local build. The 446-pixel viewport is the integrated browser default. Fictional states shown here are produced by the walkthrough; they are not pilot results.',styles['BodyU'])]
left=image_card(ROOT/'evidence/build-preview.jpg',max_w=238,max_h=470)
right=[Paragraph('A usable first rung needs an operating process',styles['H3U']),Paragraph('Named reviewer and deadlines precede the sample. The three fixture cases are labeled fictional. The ten-minute card is a proposed pilot threshold.',styles['BodyU']),Paragraph('Privacy gates',styles['H3U']),Paragraph('Invitation > explanation > human review > private candidate result > accuracy confirmation > recipient permission.',styles['BodyU']),Paragraph('Correction or substantive new review invalidates earlier approval and permission. An incomplete observation stays private and may be retried.',styles['BodyU']),Paragraph('Scope of proof',styles['H3U']),Paragraph('One fictional task with version, reviewer, observed revision, assistance disclosure and a named recipient. No universal score or promise of employment.',styles['BodyU'])]
t=Table([[left,right]],colWidths=[250,259]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),12)]));packet+=[t]
packet += [PageBreak(),Paragraph('12. Implementation specification',styles['H2U'])]+md(ROOT/'docs/BUILD_PROMPT.md')
packet += [Paragraph('13. Delivery provenance',styles['H2U']),Paragraph('The Packet was first committed as c3a13ed before product-source code. Version 1 was published successfully from 91adef9722b03b9f083eeb818482e2a2ecc692b3. The managed source preserves meaningful commits. Version 2 succeeded from 77c26576b0d615550f7b78622e46389f13dda773 after the portable-copy refinement. Exact deployment status is recorded in docs/DEPLOYMENT_LOG.md. The supplied Blueprint is preserved outside the app repository.',styles['BodyU']),Paragraph('Sources: Team 2 Blueprint supplied by Rodrigo; Rodrigo\'s final individual Brain brief; actual app and Git history. Operating references: Riipen Educators (https://www.riipen.com/educators), Forage (https://www.theforage.com/) and official Gemini text-generation documentation (https://ai.google.dev/gemini-api/docs/text-generation). These references do not validate the proposed pilot.',styles['CaptionU'])]
gemini=json.loads((ROOT/'evidence/GEMINI_LIVE_SCOPE.json').read_text())
packet += [PageBreak(),Paragraph('14. Verified live Gemini drafting',styles['H2U']),callout('Observed in the published application on 7 October 2026. Model: Gemini 3.5 Flash-Lite. Server secret masked in Sites; billing not activated. No candidate data sent.'),Spacer(1,12)]
gemini_left=image_card(ROOT/'evidence/gemini-live.jpg',max_w=238,max_h=470)
gemini_right=[Paragraph('Actual generated scope',styles['H3U']),Paragraph(markup(gemini['scope']),styles['SmallU']),Paragraph('Review and limits',styles['H3U']),Paragraph('Codex simulated an operator review and clarified an ambiguity in the first real draft. The second real response asks for both calculations without supplying their answers. A human operator must still review every draft before inviting a candidate. No invitation or human assessment was created in this check.',styles['SmallU'])]
gemini_table=Table([[gemini_left,gemini_right]],colWidths=[250,259]);gemini_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),12)]))
packet += [gemini_table,Spacer(1,10),Paragraph('Evidence: GEMINI_LIVE_FIRST_SCOPE.json and GEMINI_LIVE_SCOPE.json. Version 4 / source 5e3eae7 / environment revision 1. Exact publication results are recorded in DEPLOYMENT_LOG.md.',styles['CaptionU'])]
packet += [PageBreak(),Paragraph('Workflow diagram',styles['H2U']),Paragraph('Visual companion to the exact Mermaid flowchart source above. Added during the post-build audit.',styles['CaptionU']),workflow_diagram(),PageBreak(),Paragraph('Swimlane: actor responsibilities',styles['H2U']),Paragraph('Visual companion to the Mermaid actor lanes above. Correction repeats the human review and invalidates old approval/permission.',styles['CaptionU']),lanes_diagram()]
packet += [PageBreak(),Paragraph('Image-generated mockup - post-build addition',styles['H2U']),Paragraph('Generated 8 October and refined during the audit. A labeled design concept; actual implementation screenshots and tests are separate evidence.',styles['BodyU']),image_card(ROOT/'assets/umbral-imagegen-mockup-2026-10-08.png',max_w=509,max_h=430),Spacer(1,12),Paragraph('Image-generation provenance and prompt are retained in assets/MOCKUP_PROVENANCE.md. The concept is not a claim of a live team meeting, real review or production authentication.',styles['CaptionU'])]
build('PACKET_Rodrigo_Pena_WEEK9.pdf','Business Bending Packet',packet)

if '--packet-only' in sys.argv:
    print('Updated Packet PDF.')
    raise SystemExit(0)

styles['BodyU'].fontSize=10
styles['BodyU'].leading=14.2
styles['BodyU'].spaceAfter=7
styles['H2U'].spaceBefore=11
persona=intro('UMBRAL','Fresh Synthetic Persona / Ordered screenshots / Retest','New Google AI Studio chat, 11 October 2026. Six real fictional-app screenshots; original response, actual copy/layout fix and visual retest. No human participant or hiring validation.')+md(ROOT/'docs/PERSONA_REPORT.md')
# Selected legible screenshot portions; full originals are included with the local audit sources.
from PIL import Image as PILImage
cropdir=ROOT/'tmp/pdfs/persona-crops';cropdir.mkdir(parents=True,exist_ok=True)
items=[('1. Task','02-task.jpg','top'),('2. Candidate explanation','04-candidate.jpg','bottom'),('3. Private result','06-private.jpg','bottom'),('4. Correction','07-correction.jpg','all'),('5. Recipient permission','09-permission.jpg','all'),('6. Printable proof','11-proof.jpg','top')]
for i in range(0,len(items),2):
    persona += [PageBreak(),Paragraph('Ordered screenshot evidence',styles['H2U']),Paragraph('Actual screenshots supplied to Gemini. Tall screens are shown as labeled crops for legibility; the full original files were sent to the model and remain in the evidence folder.',styles['CaptionU'])]
    cells=[]
    for label,name,section in items[i:i+2]:
        im=PILImage.open(ROOT/'output/video/captures'/name);w,h=im.size
        if section=='top':box=(0,0,w,min(h,1050))
        elif section=='bottom':box=(0,max(0,h-1050),w,h)
        else:box=(0,0,w,h)
        target=cropdir/name;im.crop(box).save(target)
        cells.append([Paragraph(label,styles['H3U']),image_card(target,max_w=245,max_h=550),Spacer(1,8),Paragraph(name+' / '+section+' portion',styles['CaptionU'])])
    t=Table([cells],colWidths=[254.5,254.5]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0)]));persona.append(t)
persona += [PageBreak(),Paragraph('Retest: corrected private-result card',styles['H2U']),Paragraph('Actual updated local app, Ruth UM-001. The new capture was supplied to the same fresh persona chat. Software behavior and storage cannot be established by a static image.',styles['CaptionU'])]
im=PILImage.open(ROOT/'evidence/persona-after-private.jpg');w,h=im.size;target=cropdir/'after.jpg';im.crop((0,max(0,h-1000),w,h)).save(target)
persona += [image_card(target,max_w=310,max_h=530),Spacer(1,10),callout('Retest conclusion: the model accurately separates confirmation from sharing and recognizes a private ending. Fear persists; next-step and storage uncertainty remain. No complete usability validation is claimed.')]
persona += [PageBreak(),Paragraph('Original model responses',styles['H2U']),Paragraph('Direct export from the visible Gemini responses. Content is preserved, including the model misread heading and remaining doubts. Source DOM, prompts and full images are retained locally.',styles['CaptionU'])]
for line in (ROOT/'docs/PERSONA_ORIGINAL_RESPONSES.txt').read_text().splitlines():
    if line.strip():persona.append(Paragraph(escape(line),styles['RawU']))
build('PERSONA_Rodrigo_Pena_WEEK9.pdf','Fresh Synthetic Persona Report',persona)
# Genuine visible-message exports stay outside public app source.
audit=ROOT.parent.parent/'revision_2026_10_08'
if not (audit/'sources/RAW_EXPORT_PROVENANCE.json').exists():
    print('Updated report PDFs. Private raw export sources are available only in the original local workspace.');raise SystemExit(0)
provenance=json.loads((audit/'sources/RAW_EXPORT_PROVENANCE.json').read_text())
for kind in ['CHAT','BUILDCHAT']:
    name=kind+'_Rodrigo_Pena_WEEK9'; messages=json.loads((audit/'sources'/(name+'.json')).read_text())
    note=('Original visible Brain preparation exchange, followed by the unchanged 18-page ChatGPT research export. That research was operated by Codex and retains its simulated-position labels; neither section certifies a personal 40-minute research fight.' if kind=='CHAT' else 'Original visible development exchange recovered from this actual Codex chat. No reconstructed dialogue. Original tool inputs accompany the upload package; tool internals, binary media and hidden reasoning are excluded.')
    story=intro('UMBRAL',kind+' / Original visible conversation',note)
    story += [Paragraph('Source session: '+provenance['session_id'],styles['CaptionU']),Paragraph('Export cutoff (UTC): '+provenance['cutoff_utc'],styles['CaptionU']),Paragraph('Source SHA-256: '+provenance['source_sha256'],styles['CaptionU']),Paragraph(str(len(messages))+' original visible messages in this range. Machine timestamps and text are retained; ambient context remains identified in its original message.',styles['BodyU'])]
    for i,m in enumerate(messages):
        story.append(Paragraph(str(i+1)+'. '+m['role'].upper()+' / '+m['timestamp'],styles['H3U']))
        for line in m['text'].split('\n'):
            story.append(Paragraph(escape(line) if line else '&#160;',styles['RawU']))
    destination=OUT if kind=='BUILDCHAT' else ROOT.parent.parent/'01_brain_bending'
    if kind=='CHAT':
        saved=OUT;OUT=destination
    build(name+'.pdf',kind+' original visible conversation',story)
    if kind=='CHAT':
        from pypdf import PdfReader, PdfWriter
        research=ROOT.parent.parent/'01_brain_bending/CHAT_WEEK9_CODEX_SIMULATED_RAW.pdf'
        if research.exists():
            target=destination/(name+'.pdf');writer=PdfWriter()
            for source in [target,research]:
                for page in PdfReader(source).pages:writer.add_page(page)
            writer.add_metadata({'/Title':'Week 9 Brain - original preparation and Codex-operated research exports','/Author':'Rodrigo Peña de León','/Subject':'Actual visible exports; synthetic research positions disclosed'})
            with target.open('wb') as f:writer.write(f)
        OUT=saved
print('Updated Packet/Persona and exported original CHAT/BUILDCHAT PDFs.')
