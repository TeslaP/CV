from pathlib import Path
import re
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
FONT=Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('CV',str(FONT/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('CVBold',str(FONT/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('CV',normal='CV',bold='CVBold',italic='CV',boldItalic='CVBold')
navy=colors.HexColor('#17344A'); grey=colors.HexColor('#52616C')
styles={k:ParagraphStyle(k,fontName='CVBold' if k in ['name','section','role'] else 'CV',fontSize=size,leading=lead,textColor=navy if k in ['name','section','role'] else colors.HexColor('#222222'),spaceBefore=before,spaceAfter=after,keepWithNext=k in ['section','role','date']) for k,size,lead,before,after in [('name',24,29,0,7),('section',10,14,10,7),('role',10.5,14,7,3),('date',8.5,11,0,7),('body',9.2,13,0,6)]}
styles['bullet']=ParagraphStyle('bullet',parent=styles['body'],leftIndent=10,firstLineIndent=-10)
def markup(t):
 t=escape(t)
 t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<link href="\2">\1</link>',t)
 t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
 return t.replace(' * ',' • ').replace(' -- ',' - ')
s=[]
for line in Path(__file__).with_name('README.md').read_text().splitlines():
 if not line.strip() or line=='---':continue
 if line=='### Miro | Strategic Programs Lead':s.append(PageBreak())
 if line.startswith('# '):k='name';line=line[2:]
 elif line.startswith('## '):k='section';line=line[3:]
 elif line.startswith('### '):k='role';line=line[4:]
 elif line.startswith('* '):k='bullet';line='• '+line[2:]
 elif line.startswith('**') and (line.endswith('**') or line.endswith('**  ')) and ('Present' in line or re.search(r'20\d\d',line)):k='date'
 else:k='body'
 s.append(Paragraph(markup(line),styles[k]))
def footer(c,d):
 c.setStrokeColor(colors.HexColor('#DAE1E6'));c.line(42,36,553,36)
 c.setFont('CV',8);c.setFillColor(grey);c.drawString(42,23,'Pavel Teslenko | Product Lead');c.drawRightString(553,23,str(d.page))
SimpleDocTemplate(str(Path(__file__).with_name('Pavel_Teslenko_CV.pdf')),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=35,bottomMargin=48,title='Pavel Teslenko - Product Lead CV',author='Pavel Teslenko').build(s,onFirstPage=footer,onLaterPages=footer)
