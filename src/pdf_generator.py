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
from .cv_templates import get_template, get_template_by_display_name


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


def generate_pdf(content: str, title: str = "CV", template: str = "modern") -> bytes:
    """
    Genera un PDF profesional con diseño mejorado y template personalizable.
    
    Args:
        content: Texto del CV en formato markdown
        title: Título del documento
        template: Nombre del template (classic, modern, minimal, creative)
    
    Returns:
        bytes: Contenido del PDF en bytes
    """
    
    # Obtener configuración del template
    tmpl = get_template(template)
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
    
    # Estilos tipográficos basados en el template
    styles = getSampleStyleSheet()
    
    # Estilo para nombre (header principal)
    styles.add(ParagraphStyle(
        name='CVName',
        parent=styles['Heading1'],
        fontSize=tmpl.font_sizes['name'],
        textColor=tmpl.colors['primary'],
        spaceAfter=3,
        spaceBefore=0,
        alignment=TA_CENTER,
        fontName=tmpl.fonts['bold']
    ))
    
    # Estilo para titular profesional
    styles.add(ParagraphStyle(
        name='CVTitle',
        parent=styles['Normal'],
        fontSize=tmpl.font_sizes['title'],
        textColor=tmpl.colors.get('accent', tmpl.colors['primary']),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName=tmpl.fonts['main']
    ))
    
    # Estilo para información de contacto
    styles.add(ParagraphStyle(
        name='ContactInfo',
        parent=styles['Normal'],
        fontSize=tmpl.font_sizes['contact'],
        textColor=tmpl.colors['secondary'],
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName=tmpl.fonts['main']
    ))
    
    # Estilo para títulos de sección
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading2'],
        fontSize=tmpl.font_sizes['section'],
        textColor=tmpl.colors.get('accent', tmpl.colors['primary']),
        spaceAfter=6,
        spaceBefore=10,
        alignment=TA_LEFT,
        fontName=tmpl.fonts['bold'],
        borderPadding=(0, 0, 4, 0)
    ))
    
    # Estilo para subtítulos (empresa/puesto)
    styles.add(ParagraphStyle(
        name='SubHeading',
        parent=styles['Normal'],
        fontSize=tmpl.font_sizes['subheading'],
        textColor=tmpl.colors['primary'],
        spaceAfter=2,
        spaceBefore=4,
        alignment=TA_LEFT,
        fontName=tmpl.fonts['bold']
    ))
    
    # Estilo para texto secundario (fechas, ubicación)
    styles.add(ParagraphStyle(
        name='SecondaryText',
        parent=styles['Normal'],
        fontSize=tmpl.font_sizes['secondary'],
        textColor=tmpl.colors['secondary'],
        spaceAfter=3,
        alignment=TA_LEFT,
        fontName=tmpl.fonts['main']
    ))
    
    # Estilo para texto normal del cuerpo
    styles.add(ParagraphStyle(
        name='CVBodyText',
        parent=styles['Normal'],
        fontSize=tmpl.font_sizes['body'],
        textColor=tmpl.colors['text'],
        spaceAfter=4,
        alignment=TA_JUSTIFY,
        fontName=tmpl.fonts['main'],
        leading=12
    ))
    
    # Estilo para bullets
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['Normal'],
        fontSize=tmpl.font_sizes['body'],
        textColor=tmpl.colors['text'],
        spaceAfter=3,
        alignment=TA_LEFT,
        fontName=tmpl.fonts['main'],
        leftIndent=12,
        bulletIndent=0,
        leading=12
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
        # Inicializar lista de contacto
        contact_parts = []
        
        # Primera línea = Nombre y contacto
        if header_lines:
            name_line = header_lines[0]
            
            # Si la línea contiene |, separar nombre del resto
            if '|' in name_line:
                parts = [p.strip() for p in name_line.split('|')]
                # Primer parte no vacía es el nombre
                name = next((p for p in parts if p), "")
                # Resto son datos de contacto
                contact_parts = [p for p in parts[1:] if p]
            else:
                # Toda la línea es el nombre
                name = name_line
                contact_parts = []
            
            # Agregar nombre
            if name:
                name = escape_html(name)
                story.append(Paragraph(name, styles['CVName']))
        
        # Segunda línea puede ser titular
        if len(header_lines) > 1 and '|' not in header_lines[1]:
            title_line = escape_html(header_lines[1])
            story.append(Paragraph(title_line, styles['CVTitle']))
            contact_start = 2
        else:
            contact_start = 1
        
        # Procesar resto de líneas de contacto
        for line in header_lines[contact_start:]:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                contact_parts.extend([p for p in parts if p])
            else:
                contact_parts.append(line)
        
        # Mostrar información de contacto
        if contact_parts:
            # Filtrar duplicados y vacíos
            unique_contact = []
            for part in contact_parts:
                if part and part not in unique_contact:
                    unique_contact.append(part)
            
            if unique_contact:
                contact_text = ' • '.join(unique_contact)
                contact_text = escape_html(contact_text)
                story.append(Paragraph(contact_text, styles['ContactInfo']))
        
        # Línea divisoria después del header (si el template lo usa)
        if tmpl.use_dividers:
            story.append(Spacer(1, 0.05*inch))
            story.append(create_divider_line(template=tmpl))
            story.append(Spacer(1, tmpl.spacing['section']*inch))
    
    # Procesar resto del contenido
    current_section = []
    
    for line in lines[content_start_idx:]:
        line = line.strip()
        
        if not line:
            if current_section:
                story.extend(current_section)
                current_section = []
            story.append(Spacer(1, 0.05*inch))
            continue
        
        # Detectar sección (título con **)
        if line.startswith('**') and line.endswith('**'):
            # Agregar sección anterior
            if current_section:
                story.extend(current_section)
                current_section = []
            
            # Título de sección con línea
            section_title = line.strip('*').strip()
            section_title = escape_html(section_title)
            
            story.append(Spacer(1, 0.03*inch))
            story.append(Paragraph(section_title, styles['SectionHeading']))
            if tmpl.use_dividers:
                story.append(create_divider_line(template=tmpl, section=True))
            story.append(Spacer(1, tmpl.spacing['subsection']*inch))
            
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
            # Bullet con color del template
            accent_color = tmpl.colors.get('accent', tmpl.colors['primary'])
            bullet_text = f'<font color="{accent_color.hexval()}">•</font> {text}'
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


def create_divider_line(template=None, section=False):
    """
    Crea una línea divisoria horizontal usando Table.
    
    Args:
        template: CVTemplate con configuración de estilo
        section: Si True, usa estilo de sección (más grueso)
    
    Returns:
        Table con la línea divisoria
    """
    if template is None:
        from .cv_templates import MODERN_TEMPLATE
        template = MODERN_TEMPLATE
    
    # Determinar grosor y color según el template
    if template.divider_style == "thin":
        width = 0.5 if not section else 1
    elif template.divider_style == "bold":
        width = 2 if not section else 3
    elif template.divider_style == "colored":
        width = 1 if not section else 2
    else:  # none
        return Spacer(1, 0)
    
    color = template.colors.get('accent', template.colors['divider']) if section else template.colors['divider']
    
    line_table = Table([['']], colWidths=[6.5*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), width, color),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return line_table
