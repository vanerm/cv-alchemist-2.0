# src/ui_styles.py

"""
Módulo de estilos personalizados para la UI de Streamlit.
Incluye CSS custom, theming y componentes visuales.
"""

import streamlit as st


def apply_custom_styles():
    """Aplica estilos CSS personalizados a la aplicación."""
    st.markdown("""
        <style>
        /* ========== Variables de Color ========== */
        :root {
            --primary-color: #667eea;
            --primary-dark: #764ba2;
            --secondary-color: #2C3E50;
            --success-color: #27AE60;
            --warning-color: #F39C12;
            --danger-color: #E74C3C;
            --info-color: #3498DB;
            --light-bg: #f8f9fa;
            --lavender-light: #ede9fe;
            --lavender-lighter: #f3f0ff;
            --lavender-border: #c4b5fd;
            --card-shadow: 0 2px 10px rgba(102, 126, 234, 0.15);
        }
        
        /* ========== Configuración General ========== */
        .main {
            padding: 2rem 1rem;
        }
        
        /* Asegurar que todo el texto sea visible */
        .main * {
            color: inherit;
        }
        
        /* Texto principal oscuro */
        .main p, .main span, .main label {
            color: #2C3E50;
        }
        
        /* ========== Header Principal ========== */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .main-header p {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.95;
        }
        
        /* ========== Botones Mejorados ========== */
        .stButton>button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* Botón deshabilitado - mantener gradiente con opacidad */
        .stButton>button:disabled,
        .stButton>button[disabled] {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            opacity: 0.5 !important;
            cursor: not-allowed !important;
            border: none !important;
        }
        
        /* ========== Download Buttons ========== */
        .stDownloadButton>button {
            background: linear-gradient(90deg, #27AE60 0%, #229954 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
        }
        
        .stDownloadButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
        }
        
        /* ========== Cards con Sombra ========== */
        .card {
            background: var(--lavender-lighter);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: var(--card-shadow);
            margin-bottom: 1.5rem;
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        .card-header {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--secondary-color);
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--primary-color);
        }
        
        /* ========== Progress Bar Personalizada ========== */
        .stProgress > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        /* ========== Tabs Mejoradas ========== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 12px 24px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border: none;
        }
        
        /* ========== Sidebar Mejorada ========== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }
        
        /* Texto en sidebar */
        [data-testid="stSidebar"] * {
            color: #2C3E50;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #2C3E50 !important;
        }
        
        [data-testid="stSidebar"] a {
            color: #667eea !important;
            font-weight: 600;
        }
        
        [data-testid="stSidebar"] a:hover {
            color: #764ba2 !important;
        }
        
        /* ========== Métricas con Estilo ========== */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        [data-testid="stMetricDelta"] {
            font-weight: 600;
        }
        
        /* Icono de ayuda en métricas - mejor contraste */
        [data-testid="stMetric"] [data-testid="stTooltipIcon"],
        [data-testid="stMetric"] svg {
            color: #667eea !important;
            fill: #667eea !important;
        }
        
        /* ========== Alertas Personalizadas ========== */
        .stAlert {
            border-radius: 8px;
            border-left: 4px solid;
            padding: 1rem;
        }
        
        /* Success */
        [data-baseweb="notification"][kind="success"] {
            border-left-color: var(--success-color);
            background-color: #d4edda;
        }
        
        /* Info */
        [data-baseweb="notification"][kind="info"] {
            border-left-color: var(--info-color);
            background-color: #d1ecf1;
        }
        
        /* Warning */
        [data-baseweb="notification"][kind="warning"] {
            border-left-color: var(--warning-color);
            background-color: #fff3cd;
        }
        
        /* Error */
        [data-baseweb="notification"][kind="error"] {
            border-left-color: var(--danger-color);
            background-color: #f8d7da;
        }
        
        /* ========== Text Areas Mejoradas ========== */
        .stTextArea textarea {
            border-radius: 8px;
            border: 2px solid #e9ecef;
            font-family: 'Courier New', monospace;
        }
        
        .stTextArea textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        /* ========== File Uploader ========== */
        [data-testid="stFileUploader"] {
            border: 2px dashed #dee2e6;
            border-radius: 12px;
            padding: 2rem;
            background-color: var(--lavender-light);
            transition: all 0.3s ease;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: var(--primary-color);
            background-color: #f0f2ff;
        }
        
        /* Texto del file uploader */
        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] p,
        [data-testid="stFileUploader"] small {
            color: #2C3E50 !important;
        }
        
        [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {
            color: #2C3E50 !important;
        }
        
        /* Zona de drop del file uploader - fondo lila pastel */
        [data-testid="stFileUploader"] section {
            background-color: var(--lavender-lighter) !important;
            border: 2px dashed var(--lavender-border) !important;
        }
        
        [data-testid="stFileUploader"] section:hover {
            background-color: #f0f2ff !important;
            border-color: var(--primary-color) !important;
        }
        
        /* Texto dentro de la zona de drop */
        [data-testid="stFileUploader"] section span,
        [data-testid="stFileUploader"] section small,
        [data-testid="stFileUploader"] section p {
            color: #6c757d !important;
        }
        
        /* Archivos cargados - nombre y tamaño */
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
            background-color: var(--lavender-lighter) !important;
            border: 1px solid var(--lavender-border) !important;
        }
        
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] span,
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] p,
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] small {
            color: #2C3E50 !important;
        }
        
        /* Nombre del archivo cargado */
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
            color: #2C3E50 !important;
            font-weight: 500 !important;
        }
        
        /* Tamaño del archivo */
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFileSize"] {
            color: #6c757d !important;
        }
        
        /* Botón de borrar archivo (cruz X) - color por defecto gris oscuro */
        [data-testid="stFileUploader"] button[kind="icon"],
        [data-testid="stFileUploader"] button[aria-label*="Remove"],
        [data-testid="stFileUploader"] button[aria-label*="Delete"],
        [data-testid="stFileUploader"] button svg {
            color: #495057 !important;
            fill: #495057 !important;
        }
        
        /* Botón de borrar en hover - rojo */
        [data-testid="stFileUploader"] button[kind="icon"]:hover,
        [data-testid="stFileUploader"] button[aria-label*="Remove"]:hover,
        [data-testid="stFileUploader"] button[aria-label*="Delete"]:hover,
        [data-testid="stFileUploader"] button:hover svg {
            color: #E74C3C !important;
            fill: #E74C3C !important;
        }
        
        /* Flechas de navegación < y > - color por defecto gris oscuro */
        [data-testid="stFileUploader"] button[data-testid*="nav"],
        [data-testid="stFileUploader"] button[aria-label*="Previous"],
        [data-testid="stFileUploader"] button[aria-label*="Next"],
        [data-testid="stFileUploader"] button[aria-label*="Anterior"],
        [data-testid="stFileUploader"] button[aria-label*="Siguiente"] {
            color: #495057 !important;
        }
        
        [data-testid="stFileUploader"] button[data-testid*="nav"] svg,
        [data-testid="stFileUploader"] button[aria-label*="Previous"] svg,
        [data-testid="stFileUploader"] button[aria-label*="Next"] svg,
        [data-testid="stFileUploader"] button[aria-label*="Anterior"] svg,
        [data-testid="stFileUploader"] button[aria-label*="Siguiente"] svg {
            fill: #495057 !important;
        }
        
        /* Flechas de navegación en hover - rojo */
        [data-testid="stFileUploader"] button[data-testid*="nav"]:hover,
        [data-testid="stFileUploader"] button[aria-label*="Previous"]:hover,
        [data-testid="stFileUploader"] button[aria-label*="Next"]:hover,
        [data-testid="stFileUploader"] button[aria-label*="Anterior"]:hover,
        [data-testid="stFileUploader"] button[aria-label*="Siguiente"]:hover {
            color: #E74C3C !important;
        }
        
        [data-testid="stFileUploader"] button[data-testid*="nav"]:hover svg,
        [data-testid="stFileUploader"] button[aria-label*="Previous"]:hover svg,
        [data-testid="stFileUploader"] button[aria-label*="Next"]:hover svg,
        [data-testid="stFileUploader"] button[aria-label*="Anterior"]:hover svg,
        [data-testid="stFileUploader"] button[aria-label*="Siguiente"]:hover svg {
            fill: #E74C3C !important;
        }
        
        /* ========== Selectbox Mejorado ========== */
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 2px solid #e9ecef;
        }
        
        .stSelectbox > div > div:focus-within {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        /* ========== Expander Mejorado ========== */
        [data-testid="stExpander"] {
            background-color: var(--lavender-lighter) !important;
            border: 1px solid var(--lavender-border) !important;
            border-radius: 8px !important;
        }
        
        [data-testid="stExpander"] summary {
            background-color: var(--lavender-lighter) !important;
            border-radius: 8px;
            font-weight: 600;
            padding: 1rem;
            color: #2C3E50 !important;
        }
        
        [data-testid="stExpander"] summary:hover {
            background-color: var(--lavender-light) !important;
        }
        
        /* Contenido del expander - FONDO BLANCO Y TEXTO OSCURO */
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
            background-color: #ffffff !important;
            padding: 1rem;
        }
        
        /* FORZAR texto oscuro en TODO el contenido */
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] *,
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] span,
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] div,
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] strong,
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMarkdown"],
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] [data-testid="stMarkdown"] *,
        [data-testid="stExpander"] div[data-testid="stMarkdownContainer"],
        [data-testid="stExpander"] div[data-testid="stMarkdownContainer"] * {
            color: #2C3E50 !important;
        }
        
        /* Expanders en sidebar - fondo lila pastel en TODOS los estados */
        [data-testid="stSidebar"] [data-testid="stExpander"],
        [data-testid="stSidebar"] [data-testid="stExpander"][aria-expanded="true"],
        [data-testid="stSidebar"] [data-testid="stExpander"][aria-expanded="false"],
        [data-testid="stSidebar"] details,
        [data-testid="stSidebar"] details[open] {
            background-color: var(--lavender-lighter) !important;
            border: 1px solid var(--lavender-border) !important;
        }
        
        [data-testid="stSidebar"] .streamlit-expanderHeader,
        [data-testid="stSidebar"] details[open] .streamlit-expanderHeader {
            background-color: var(--lavender-lighter) !important;
            color: #2C3E50 !important;
        }
        
        [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
            background-color: var(--lavender-light) !important;
        }
        
        [data-testid="stSidebar"] .streamlit-expanderHeader svg {
            fill: #2C3E50 !important;
        }
        
        [data-testid="stSidebar"] .streamlit-expanderContent {
            background-color: var(--lavender-lighter) !important;
            color: #2C3E50 !important;
        }
        
        [data-testid="stSidebar"] .streamlit-expanderContent p,
        [data-testid="stSidebar"] .streamlit-expanderContent li,
        [data-testid="stSidebar"] .streamlit-expanderContent span,
        [data-testid="stSidebar"] .streamlit-expanderContent strong {
            color: #2C3E50 !important;
        }
        
        /* Forzar details (elemento HTML nativo) */
        [data-testid="stSidebar"] details summary {
            background-color: #ffffff !important;
            color: #2C3E50 !important;
        }
        
        /* ========== Radio Buttons ========== */
        .stRadio > div {
            gap: 1rem;
        }
        
        .stRadio label {
            background-color: #f8f9fa;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: 2px solid #dee2e6;
            transition: all 0.3s ease;
        }
        
        .stRadio label:hover {
            background-color: #e9ecef;
            border-color: var(--primary-color);
        }
        
        /* Texto del radio button */
        .stRadio label span {
            color: #2C3E50 !important;
            font-weight: 500 !important;
        }
        
        .stRadio label p {
            color: #2C3E50 !important;
            font-weight: 500 !important;
        }
        
        /* Radio button seleccionado */
        .stRadio [data-baseweb="radio"] {
            background-color: white;
        }
        
        /* ========== Divider Personalizado ========== */
        hr {
            margin: 2rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #dee2e6, transparent);
        }
        
        /* ========== Animaciones ========== */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(-20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .animate-slide-in {
            animation: slideIn 0.4s ease-out;
        }
        
        /* ========== Scrollbar Personalizada ========== */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* ========== Responsive ========== */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 1.8rem;
            }
            
            .card {
                padding: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = ""):
    """Renderiza header principal con estilo."""
    st.markdown(f"""
        <div class="main-header animate-fade-in">
            <h1>🧪 {title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def render_card(content: str, header: str = ""):
    """Renderiza un card con contenido."""
    header_html = f'<div class="card-header">{header}</div>' if header else ''
    st.markdown(f"""
        <div class="card animate-fade-in">
            {header_html}
            {content}
        </div>
    """, unsafe_allow_html=True)
