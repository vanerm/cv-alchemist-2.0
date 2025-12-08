# src/pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Frame, PageTemplate, KeepTogether
)
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image, ImageDraw
import re


# Paleta de colores profesional
COLOR_PRIMARY = HexColor('#2C3E50')      # Azul oscuro
COLOR_ACCENT = HexColor('#3498DB')       # Azul
COLOR_TEXT = HexColor('#2C3E50')         # Texto principal
COLOR_SECONDARY = HexColor('#7F8C8D')    # Gris para texto secundario
COLOR_DIVIDER = HexColor('#BDC3C7')      # Líneas divisorias


def create_contact_icon(icon_type='circle', size=8, color='#3498DB'):
    """
    Crea un icono simple usando Pillow.
    
    Args:
        icon_type: Tipo de icono ('circle', 'square')
        size: Tamaño en píxeles
        color: Color en formato hex
    
    Returns:
        BytesIO con la imagen del icono
    """
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Convertir color hex a RGB
    color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    if icon_type == 'circle':
        draw.ellipse([0, 0, size-1, size-1], fill=color_rgb)
    elif icon_type == 'square':
        draw.rectangle([0, 0, size-1, size-1], fill=color_rgb)
    
    # Guardar en BytesIO
    icon_buffer = BytesIO()
    img.save(icon_buffer, format='PNG')
    icon_buffer.seek(0)
    
    return icon_buffer


def generate_pdf(content: str, title: str = "CV") -> bytes:
    """
    Genera un PDF profesional con diseño mejorado (4 fases implementadas).
    
    Fases:
    1. Tipografía y espaciado mejorado
    2. Líneas divisorias y colores
    3. Iconos simples con Pillow
    4. Layout optimizado con Platypus
    
    Args:
        content: Texto del CV en formato markdown
        title: Título del documento
    
    Returns:
        bytes: Contenido del PDF en bytes
    """
    buffer = BytesIO()
    
    # Configuración del documento con márgenes optimizados
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch,
        title=title
    )
    
    # FASE 1: Estilos tipográficos mejorados
    styles = getSampleStyleSheet()
    
    # Estilo para nombre (header principal)
    styles.add(ParagraphStyle(
        name='CVName',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=COLOR_PRIMARY,
        spaceAfter=4,
        spaceBefore=0,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para titular profesional
    styles.add(ParagraphStyle(
        name='CVTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=COLOR_ACCENT,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    
    # Estilo para información de contacto
    styles.add(ParagraphStyle(
        name='ContactInfo',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLOR_SECONDARY,
        spaceAfter=16,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    
    # Estilo para títulos de sección (con color acento)
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=COLOR_ACCENT,
        spaceAfter=8,
        spaceBefore=14,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        borderPadding=(0, 0, 4, 0)
    ))
    
    # Estilo para subtítulos (empresa/puesto)
    styles.add(ParagraphStyle(
        name='SubHeading',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLOR_PRIMARY,
        spaceAfter=3,
        spaceBefore=6,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para texto secundario (fechas, ubicación)
    styles.add(ParagraphStyle(
        name='SecondaryText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLOR_SECONDARY,
        spaceAfter=4,
        alignment=TA_LEFT,
        fontName='Helvetica'
    ))
    
    # Estilo para texto normal del cuerpo
    styles.add(ParagraphStyle(
        name='CVBodyText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_TEXT,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leading=14
    ))
    
    # Estilo para bullets
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_TEXT,
        spaceAfter=4,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leftIndent=12,
        bulletIndent=0
    ))
    
    story = []
    
    # Procesar contenido
    lines = content.split('\n')
    
    # Detectar header (primeras líneas con info de contacto)
    header_lines = []
    content_start_idx = 0
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            content_start_idx = i + 1
            break
        if '|' in line or '@' in line or any(x in line.lower() for x in ['linkedin', 'github', 'portfolio']):
            header_lines.append(line)
        else:
            if i < 3:  # Primeras 3 líneas pueden ser header
                header_lines.append(line)
            else:
                content_start_idx = i
                break
    
    # FASE 3 & 4: Procesar header con diseño mejorado
    if header_lines:
        # Primera línea = Nombre
        if header_lines:
            name_line = header_lines[0]
            # Extraer nombre (antes del primer |)
            name = name_line.split('|')[0].strip()
            name = escape_html(name)
            story.append(Paragraph(name, styles['CVName']))
        
        # Segunda línea puede ser titular
        if len(header_lines) > 1 and '|' not in header_lines[1]:
            title_line = escape_html(header_lines[1])
            story.append(Paragraph(title_line, styles['CVTitle']))
            contact_start = 2
        else:
            contact_start = 1
        
        # Resto = Contacto (combinar en una línea)
        contact_parts = []
        for line in header_lines[contact_start:]:
            parts = [p.strip() for p in line.split('|')]
            contact_parts.extend([p for p in parts if p and p not in contact_parts])
        
        if contact_parts:
            contact_text = ' • '.join(contact_parts)
            contact_text = escape_html(contact_text)
            story.append(Paragraph(contact_text, styles['ContactInfo']))
        
        # FASE 2: Línea divisoria después del header
        story.append(Spacer(1, 0.05*inch))
        story.append(create_divider_line())
        story.append(Spacer(1, 0.15*inch))
    
    # Procesar resto del contenido
    current_section = []
    
    for line in lines[content_start_idx:]:
        line = line.strip()
        
        if not line:
            if current_section:
                story.extend(current_section)
                current_section = []
            story.append(Spacer(1, 0.08*inch))
            continue
        
        # Detectar sección (título con **)
        if line.startswith('**') and line.endswith('**'):
            # Agregar sección anterior
            if current_section:
                story.extend(current_section)
                current_section = []
            
            # FASE 2: Título de sección con línea
            section_title = line.strip('*').strip()
            section_title = escape_html(section_title)
            
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph(section_title, styles['SectionHeading']))
            story.append(create_divider_line(width=2, color=COLOR_ACCENT))
            story.append(Spacer(1, 0.08*inch))
            
        # Detectar subtítulo (empresa/puesto con **)
        elif '**' in line and not line.startswith('▶'):
            text = process_markdown_bold(line)
            current_section.append(Paragraph(text, styles['SubHeading']))
            
        # Detectar texto secundario (fechas, ubicación con ·)
        elif '·' in line or '–' in line or any(month in line for month in ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre', 'Actualidad', 'Present']):
            text = escape_html(line)
            current_section.append(Paragraph(text, styles['SecondaryText']))
            
        # Detectar bullets de proyecto
        elif line.startswith('▶'):
            text = line.replace('▶', '•')
            text = process_markdown_bold(text)
            current_section.append(Paragraph(text, styles['SubHeading']))
            
        # Detectar bullets normales
        elif line.startswith('•') or line.startswith('-'):
            text = line.lstrip('•-').strip()
            text = process_markdown_bold(text)
            # FASE 3: Bullet con icono
            bullet_text = f'<font color="{COLOR_ACCENT.hexval()}">•</font> {text}'
            current_section.append(Paragraph(bullet_text, styles['BulletText']))
            
        # Texto normal
        else:
            text = process_markdown_bold(line)
            current_section.append(Paragraph(text, styles['CVBodyText']))
    
    # Agregar última sección
    if current_section:
        story.extend(current_section)
    
    # Construir PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def escape_html(text: str) -> str:
    """Escapa caracteres especiales HTML."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def process_markdown_bold(text: str) -> str:
    """
    Procesa markdown bold (**texto**) y escapa caracteres especiales.
    """
    def escape_bold_content(match):
        content = match.group(1)
        content = escape_html(content)
        return f'<b>{content}</b>'
    
    # Reemplazar bold
    text = re.sub(r'\*\*(.+?)\*\*', escape_bold_content, text)
    
    # Escapar resto del texto
    parts = re.split(r'(<b>.*?</b>)', text)
    escaped_parts = []
    for part in parts:
        if part.startswith('<b>') and part.endswith('</b>'):
            escaped_parts.append(part)
        else:
            escaped_parts.append(escape_html(part))
    
    return ''.join(escaped_parts)


def create_divider_line(width=1, color=COLOR_DIVIDER):
    """
    Crea una línea divisoria horizontal usando Table.
    
    Args:
        width: Grosor de la línea en puntos
        color: Color de la línea
    
    Returns:
        Table con la línea divisoria
    """
    line_table = Table([['']], colWidths=[6.5*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), width, color),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return line_table
