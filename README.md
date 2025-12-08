# 🧪 CV Alchemist 2.0  
Aplicación web con IA desarrollada con **Streamlit** para crear, analizar y optimizar CVs.

---

## 📌 Descripción del Proyecto

CV Alchemist 2.0 es una aplicación interactiva que permite:

- **Subir un CV existente** en formato PDF para analizarlo y extraer su contenido.  
- **Crear un CV desde cero** mediante un formulario dinámico con validación de datos.  
- **Generar un CV Maestro** actualizado integrando nueva formación con IA.  
- **Crear un Perfil de LinkedIn** optimizado a partir del CV Maestro.  
- **Generar un CV Target** personalizado para un puesto específico.  
- **Seleccionar modelo de IA** (OpenAI o Gemini) con fallback automático.
- **Analizar compatibilidad ATS** del CV generado con scoring y recomendaciones.
- **Elegir templates profesionales** para personalizar el diseño del PDF.
- **Descargar en PDF** todos los documentos generados (CV Maestro, LinkedIn, CV Target).

El proyecto forma parte del módulo **Prompt Engineering** de CoderHouse y tiene como objetivo aplicar buenas prácticas de diseño de prompts en una aplicación funcional en Python.

---

## 📑 Presentación del Proyecto (PPT)

Para ver la presentación utilizada en la pre-entrega del curso, accedé aquí:

👉 [**Google Slides**](https://docs.google.com/presentation/d/1eEIGp8-rix1Tz2_vwm3lCRcLPKQTEXyUOgclLZ90vF0/edit?usp=sharing)

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.13**
- **Streamlit** (interfaz web interactiva)
- **PyPDF2 / pdfplumber** (extracción de texto desde PDF)
- **OpenAI API** (generación de CVs con IA - primaria)
- **Google Gemini API** (fallback automático)
- **ReportLab** (generación de PDFs profesionales)
- **python-dotenv** (gestión de variables de entorno)
- **Entorno virtual venv**
- **Git & GitHub**

---

## 📂 Estructura del Proyecto

```bash
cv-alchemist-2.0/
│
├── README.md                     # Documento principal del proyecto
├── app.py                        # Aplicación principal de Streamlit
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                    # Archivos ignorados por Git
├── LICENSE                       # Licencia MIT
│
├── src/                          # Lógica y módulos internos
│   ├── extract_pdf.py            # Extracción de texto desde PDF
│   ├── form_helpers.py           # Formulario dinámico para crear CV desde cero
│   ├── ai_service.py             # Integración con OpenAI API
│   ├── prompts.py                # Prompts optimizados (Maestro, Target, LinkedIn)
│   ├── pdf_generator.py          # Generación de PDFs con ReportLab
│   ├── ats_analyzer.py           # Análisis de compatibilidad ATS
│   ├── cv_templates.py           # Templates personalizables de CV
│   ├── ui_styles.py              # Estilos CSS personalizados
│   ├── ui_components.py          # Componentes reutilizables de UI
│   ├── utils.py                  # Funciones auxiliares
│   └── __init__.py
│
├── docs/                         # Documentación del curso
│   └── preentrega/
│       └── diagramas/            # Imágenes y recursos
│
└── venv/                         # Entorno virtual (excluido de Git)

```
---

## ▶️ Cómo Ejecutarlo Localmente

### **1. Clonar el repositorio**
```bash
git clone https://github.com/vanerm/cv-alchemist-2.0.git
cd cv-alchemist-2.0
```

### **2. Crear entorno virtual**
```bash
python3 -m venv venv
```

### **3. Activar entorno virtual**
```bash
# En macOS/Linux
source venv/bin/activate
# En Windows
venv\Scripts\activate
```

### **4. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **5. Configurar variables de entorno**
Crear un archivo `.env` en la raíz del proyecto:
```bash
# API Primaria (OpenAI)
OPENAI_API_KEY=tu_openai_api_key_aqui
OPENAI_MODEL=gpt-4o-mini

# API Fallback (Gemini) - Opcional
GEMINI_API_KEY=tu_gemini_api_key_aqui
GEMINI_MODEL=gemini-1.5-flash
```

**Notas:**
- El sistema usa OpenAI por defecto
- Si OpenAI falla (límite excedido, error), automáticamente usa Gemini
- Puedes configurar solo una API key si prefieres
- Obtén las keys en:
  - OpenAI: https://platform.openai.com/api-keys
  - Gemini: https://makersuite.google.com/app/apikey
### **6. Ejecutar la aplicación**
```bash
streamlit run app.py
```
👉 Se abrirá automáticamente en: http://localhost:8501

---

## ✨ Funcionalidades Principales

### 📄 Opción 1: Subir CV Existente
1. **Carga de PDF**: Sube tu CV actual en formato PDF con validación avanzada
2. **Extracción de texto**: Procesamiento automático con pdfplumber
3. **Agregar formación**: Opcionalmente sube PDFs de nuevos cursos/certificaciones
4. **Generar CV Maestro**: IA integra la nueva formación manteniendo tu experiencia
5. **Crear Perfil LinkedIn**: Genera contenido optimizado para LinkedIn
6. **CV Target**: Personaliza tu CV para un puesto específico
7. **Análisis ATS**: Evalúa compatibilidad con sistemas de filtrado automático
8. **Descargar PDF**: Exporta cualquier documento con el template elegido

### 📝 Opción 2: Crear CV desde Cero
1. **Formulario dinámico**: Completa tus datos personales con validación en tiempo real
2. **Experiencia profesional**: Agrega hasta 10 empleos con fechas inteligentes
3. **Educación**: Incluye hasta 10 estudios con opción "En curso"
4. **Proyectos**: Destaca hasta 10 proyectos relevantes con enlaces
5. **Habilidades**: Lista tus competencias técnicas y blandas
6. **Validación de datos**: Regex para email, teléfono, URLs y sanitización de texto
7. **Generación con IA**: Crea CV Maestro, LinkedIn y CV Target
8. **Análisis ATS**: Score y recomendaciones para optimizar tu CV
9. **Exportación PDF**: Descarga todos los documentos generados

### 🤖 Selección de Modelo de IA
- **Selector en sidebar**: Elige entre OpenAI, Gemini o modo Auto
- **Múltiples modelos OpenAI**: gpt-4o-mini, gpt-4o, gpt-4-turbo-preview, gpt-3.5-turbo
- **Múltiples modelos Gemini**: gemini-flash-latest, gemini-2.5-flash, gemini-2.5-pro, gemini-pro-latest
- **Fallback automático**: Si OpenAI falla, usa Gemini automáticamente
- **Mensajes dinámicos**: El spinner muestra el modelo específico en uso
- **Logs de debugging**: Seguimiento detallado en consola

### 🎨 Templates Profesionales
- **Clásico**: Formato tradicional (ATS ⭐⭐⭐⭐⭐) - Ideal para Legal, Finanzas
- **Moderno**: Balance diseño/parseabilidad (ATS ⭐⭐⭐⭐) - Ideal para Tech, Startups
- **Minimalista**: Espaciado generoso (ATS ⭐⭐⭐⭐) - Ideal para Diseño, UX/UI
- **Creativo**: Más visual (ATS ⭐⭐⭐) - Ideal para Marketing, Publicidad
- **Personalización**: Tipografía, colores, iconos y layout profesional

### 🔍 Análisis ATS Avanzado
- **Scoring 0-100**: Evaluación cuantitativa de compatibilidad
- **4 Criterios**: Formato (25%), Palabras clave (40%), Contenido (20%), Optimización (15%)
- **Palabras clave**: Identificación de términos encontrados y faltantes
- **Fortalezas y debilidades**: Análisis detallado por categoría
- **Recomendaciones accionables**: Sugerencias específicas para mejorar
- **Detalles por criterio**: Información expandible para cada métrica

### 🤖 Prompts Inteligentes
- **Prompt Maestro**: Integra nueva formación sin inventar experiencia
- **Prompt Target**: Personaliza CV sin alucinaciones, respetando la verdad
- **Prompt LinkedIn**: Genera perfil profesional optimizado
- **Prompt ATS**: Analiza compatibilidad con sistemas de reclutamiento
- **Anti-alucinaciones**: Reglas estrictas para mantener veracidad

### 🛡️ Seguridad y Validación
- **Validación de email**: Regex para formato válido con @ y dominio
- **Validación de teléfono**: Solo números, +, -, ( ) con longitud mínima/máxima
- **Validación de URLs**: Formato http/https con dominio válido
- **Validación de nombres**: Solo letras, espacios, acentos, apóstrofes y guiones
- **Sanitización de texto**: Remoción de caracteres de control y peligrosos
- **Validación de PDFs**: Tamaño, tipo, protección y contenido legible
- **Mensajes de error detallados**: Feedback específico para cada campo

### 🎨 Interfaz de Usuario
- **Sidebar interactivo**: Progreso, estadísticas, selección de modelo
- **Tema lila pastel**: Diseño consistente y profesional
- **Indicadores de progreso**: Checkmarks verdes para pasos completados
- **Botón reiniciar**: Limpia sesión sin recargar página
- **Mensajes contextuales**: Success, info, warning y error con iconos
- **Responsive**: Adaptable a diferentes tamaños de pantalla

---

## 🧱 Versión Anterior del Proyecto (MVP – Prompt Engineering I)

Este proyecto es una evolución de la primera versión del MVP desarrollada durante el curso Prompt Engineering I.

Podés ver el repositorio original aquí:  
👉 [cv-alchemist (MVP 2025)](https://github.com/vanerm/cv-alchemist)

La versión 2.0 incorpora nuevas funcionalidades, mejor arquitectura interna y un enfoque más completo para la creación y optimización de CVs utilizando IA.

---

## 🚧 Estado Actual del Proyecto

- [x] Estructura base funcionando  
- [x] Interfaz Streamlit operativa  
- [x] Extracción de texto desde PDF con pdfplumber
- [x] Formulario dinámico "Crear CV desde cero" con campos de fecha inteligentes
- [x] Integración con OpenAI API para generación de CVs
- [x] Fallback automático a Gemini API si OpenAI falla
- [x] Generación de CV Maestro con IA
- [x] Generación de Perfil LinkedIn optimizado
- [x] Generación de CV Target personalizado por puesto
- [x] Exportación a PDF de todos los documentos generados
- [x] Prompts ultra estrictos para evitar alucinaciones de IA
- [x] Validación avanzada de archivos PDF (tamaño, tipo, protección, contenido)
- [x] Diseño visual profesional de PDFs (tipografía, colores, iconos, layout)
- [x] Templates personalizables (Clásico, Moderno, Minimalista, Creativo)
- [x] Análisis ATS con scoring, palabras clave y recomendaciones
- [x] Selector de modelo de IA en sidebar (OpenAI/Gemini/Auto)
- [x] Múltiples modelos disponibles por proveedor
- [x] Validación de formulario con regex (email, teléfono, URLs)
- [x] Sanitización de inputs para prevenir inyección de código
- [x] Mensajes de spinner dinámicos mostrando modelo en uso
- [x] Sidebar con indicadores de progreso y estadísticas
- [x] Botón reiniciar para limpiar sesión
- [x] Tema visual consistente (lila pastel) en toda la UI
- [x] Script de prueba de APIs (test_apis.py)

---

## 🧭 Roadmap / Próximos Pasos

- [ ] Deploy de la app en Streamlit Community Cloud
- [ ] Agregar soporte para más idiomas (inglés, portugués)
- [ ] Implementar historial de CVs generados
- [ ] Agregar exportación en formato Word (.docx)
- [ ] Integrar más modelos de IA (Claude, Llama)
- [ ] Crear sistema de plantillas personalizadas por usuario

---

## 🎓 Propósito Educativo

Este proyecto se desarrolla como parte del curso **Prompt Engineering para Programadores – CoderHouse**.

El objetivo principal es practicar:

- **Diseño y optimización de prompts** con reglas anti-alucinaciones
- **Integración de IA en aplicaciones reales** (OpenAI API)
- **Modularización limpia** y arquitectura escalable
- **Creación de interfaces funcionales** con Streamlit
- **Generación de documentos** con ReportLab

---

## 📄 Licencia
El proyecto está disponible bajo la licencia MIT, permitiendo su uso libre para fines personales, académicos o experimentales.
Para más detalles, consulta el archivo LICENSE.

---

## ✋ About Me

Soy **Vanesa Mizrahi**, desarrolladora de software iOS y **Data Scientist en formación**.  
Trabajo con Python, SQL y técnicas de Machine Learning para crear soluciones prácticas orientadas a negocio, incluyendo aplicaciones interactivas con **Streamlit** y flujos basados en IA generativa.

Me interesa especialmente:
- Análisis exploratorio y visualización de datos  
- Modelos de ML aplicados a problemas reales  
- Diseño de prompts y uso de APIs de IA  
- Desarrollo de herramientas que integren datos + experiencia de usuario  

Actualmente continúo mi especialización a través de la Diplomatura en Data Science [CoderHouse](https://www.coderhouse.com/ar/diplomaturas/data/?pipe_source=google&pipe_medium=cpc&pipe_campaign=1&gad_source=1&gad_campaignid=13952864596&gbraid=0AAAAACoxfTL7S4LjLGDCtBrigIZUvaOtI&gclid=CjwKCAiAxc_JBhA2EiwAFVs7XJlquLs6YOrHV_5FBSUgw11RG-8BGH6YVHXJN2QfehgVqOBGVghiqxoCOQsQAvD_BwE).

🔗 **LinkedIn:** [Vanesa Mizrahi](https://www.linkedin.com/in/vanesamizrahi)
