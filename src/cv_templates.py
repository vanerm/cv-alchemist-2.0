# src/cv_templates.py

from reportlab.lib.colors import HexColor
from dataclasses import dataclass
from typing import Dict


@dataclass
class CVTemplate:
    """Clase que define un template de CV con sus características visuales."""
    
    name: str
    display_name: str
    description: str
    colors: Dict[str, HexColor]
    fonts: Dict[str, str]
    layout: str
    font_sizes: Dict[str, int]
    spacing: Dict[str, float]
    use_dividers: bool
    divider_style: str


# Template Clásico - Formal y tradicional
CLASSIC_TEMPLATE = CVTemplate(
    name="classic",
    display_name="Clásico",
    description="Formal y tradicional. Ideal para sectores conservadores (legal, finanzas, gobierno).",
    colors={
        "primary": HexColor('#000000'),
        "secondary": HexColor('#666666'),
        "text": HexColor('#000000'),
        "divider": HexColor('#000000'),
    },
    fonts={
        "main": "Times-Roman",
        "bold": "Times-Bold",
        "italic": "Times-Italic",
    },
    layout="single_column",
    font_sizes={
        "name": 16,
        "title": 10,
        "contact": 8,
        "section": 11,
        "subheading": 9,
        "body": 9,
        "secondary": 8,
    },
    spacing={
        "section": 0.1,
        "subsection": 0.06,
        "paragraph": 0.04,
    },
    use_dividers=True,
    divider_style="thin"
)


# Template Moderno - Actual, con colores
MODERN_TEMPLATE = CVTemplate(
    name="modern",
    display_name="Moderno",
    description="Profesional y actual. Ideal para tech, startups y empresas innovadoras.",
    colors={
        "primary": HexColor('#2C3E50'),
        "accent": HexColor('#3498DB'),
        "text": HexColor('#2C3E50'),
        "secondary": HexColor('#7F8C8D'),
        "divider": HexColor('#BDC3C7'),
    },
    fonts={
        "main": "Helvetica",
        "bold": "Helvetica-Bold",
        "italic": "Helvetica-Oblique",
    },
    layout="single_column_emphasis",
    font_sizes={
        "name": 18,
        "title": 11,
        "contact": 8,
        "section": 12,
        "subheading": 10,
        "body": 9,
        "secondary": 8,
    },
    spacing={
        "section": 0.08,
        "subsection": 0.05,
        "paragraph": 0.03,
    },
    use_dividers=True,
    divider_style="colored"
)


# Template Minimalista - Limpio y espacioso
MINIMAL_TEMPLATE = CVTemplate(
    name="minimal",
    display_name="Minimalista",
    description="Limpio y elegante. Ideal para diseño, UX/UI y portfolios creativos.",
    colors={
        "primary": HexColor('#000000'),
        "accent": HexColor('#000000'),
        "text": HexColor('#000000'),
        "secondary": HexColor('#666666'),
        "divider": HexColor('#E0E0E0'),
    },
    fonts={
        "main": "Helvetica",
        "bold": "Helvetica-Bold",
        "italic": "Helvetica-Oblique",
    },
    layout="single_column_spacious",
    font_sizes={
        "name": 20,
        "title": 10,
        "contact": 8,
        "section": 10,
        "subheading": 9,
        "body": 9,
        "secondary": 8,
    },
    spacing={
        "section": 0.12,
        "subsection": 0.08,
        "paragraph": 0.05,
    },
    use_dividers=False,
    divider_style="none"
)


# Template Creativo - Vibrante y llamativo
CREATIVE_TEMPLATE = CVTemplate(
    name="creative",
    display_name="Creativo",
    description="Vibrante y llamativo. Ideal para marketing, publicidad y roles creativos.",
    colors={
        "primary": HexColor('#2C3E50'),
        "accent": HexColor('#E74C3C'),
        "text": HexColor('#2C3E50'),
        "secondary": HexColor('#95A5A6'),
        "divider": HexColor('#E74C3C'),
    },
    fonts={
        "main": "Helvetica",
        "bold": "Helvetica-Bold",
        "italic": "Helvetica-Oblique",
    },
    layout="single_column_bold",
    font_sizes={
        "name": 22,
        "title": 12,
        "contact": 9,
        "section": 13,
        "subheading": 10,
        "body": 9,
        "secondary": 8,
    },
    spacing={
        "section": 0.1,
        "subsection": 0.06,
        "paragraph": 0.04,
    },
    use_dividers=True,
    divider_style="bold"
)


# Diccionario de templates disponibles
TEMPLATES = {
    "classic": CLASSIC_TEMPLATE,
    "modern": MODERN_TEMPLATE,
    "minimal": MINIMAL_TEMPLATE,
    "creative": CREATIVE_TEMPLATE,
}


def get_template(template_name: str = "modern") -> CVTemplate:
    """
    Obtiene un template por su nombre.
    
    Args:
        template_name: Nombre del template (classic, modern, minimal, creative)
    
    Returns:
        CVTemplate correspondiente, o MODERN_TEMPLATE por defecto
    """
    return TEMPLATES.get(template_name.lower(), MODERN_TEMPLATE)


def get_template_names() -> list:
    """Retorna lista de nombres de templates disponibles."""
    return [t.display_name for t in TEMPLATES.values()]


def get_template_by_display_name(display_name: str) -> CVTemplate:
    """
    Obtiene un template por su nombre de visualización.
    
    Args:
        display_name: Nombre mostrado al usuario (Clásico, Moderno, etc.)
    
    Returns:
        CVTemplate correspondiente
    """
    for template in TEMPLATES.values():
        if template.display_name == display_name:
            return template
    return MODERN_TEMPLATE
