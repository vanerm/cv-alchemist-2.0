# src/pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from io import BytesIO


def generate_pdf(content: str, title: str = "CV") -> bytes:
    """
    Genera un PDF a partir de texto plano con formato markdown básico.
    
    Args:
        content: Texto del CV en formato plano con markdown
        title: Título del documento
    
    Returns:
        bytes: Contenido del PDF en bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#2C3E50',
        spaceAfter=12,
        alignment=TA_LEFT
    ))
    
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#34495E',
        spaceAfter=8,
        spaceBefore=12,
        alignment=TA_LEFT
    ))
    
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor='#2C3E50',
        spaceAfter=6,
        alignment=TA_LEFT
    ))
    
    story = []
    
    # Procesar el contenido línea por línea
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Detectar encabezados markdown
        if line.startswith('**') and line.endswith('**'):
            # Es un encabezado
            text = line.strip('*').strip()
            # Escapar caracteres especiales
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            para = Paragraph(text, styles['CustomHeading'])
            story.append(para)
        elif line.startswith('▶'):
            # Es un proyecto
            text = line.replace('▶', '•')
            # Escapar caracteres especiales
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            para = Paragraph(text, styles['CustomBody'])
            story.append(para)
        else:
            # Texto normal
            import re
            
            # Primero extraer contenido bold y escaparlo
            def escape_bold_content(match):
                content = match.group(1)
                # Escapar caracteres especiales dentro del bold
                content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                return f'<b>{content}</b>'
            
            # Reemplazar bold con contenido escapado
            text = re.sub(r'\*\*(.+?)\*\*', escape_bold_content, line)
            
            # Escapar el resto del texto (fuera de los tags <b>)
            parts = re.split(r'(<b>.*?</b>)', text)
            escaped_parts = []
            for part in parts:
                if part.startswith('<b>') and part.endswith('</b>'):
                    escaped_parts.append(part)
                else:
                    escaped_parts.append(part.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            text = ''.join(escaped_parts)
            
            para = Paragraph(text, styles['CustomBody'])
            story.append(para)
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
