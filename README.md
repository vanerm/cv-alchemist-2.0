# 🧪 CV Alchemist 2.0  
Aplicación web con IA desarrollada con **Streamlit** para crear, analizar y optimizar CVs.

---

## 📌 Descripción del Proyecto

CV Alchemist 2.0 es una aplicación interactiva que permite:

- **Subir un CV existente** en formato PDF para analizarlo y extraer su contenido.  
- **Crear un CV desde cero** mediante un formulario dinámico con campos de fecha inteligentes.  
- **Generar un CV Maestro** actualizado integrando nueva formación con IA.  
- **Crear un Perfil de LinkedIn** optimizado a partir del CV Maestro.  
- **Generar un CV Target** personalizado para un puesto específico.  
- **Analizar compatibilidad ATS** del CV generado con scoring y recomendaciones.
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
- **OpenAI API** (generación de CVs con IA)
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
Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
OPENAI_API_KEY=tu_api_key_aqui
```
### **6. Ejecutar la aplicación**
```bash
streamlit run app.py
```
👉 Se abrirá automáticamente en: http://localhost:8501

---

## ✨ Funcionalidades Principales

### 📄 Opción 1: Subir CV Existente
1. **Carga de PDF**: Sube tu CV actual en formato PDF
2. **Extracción de texto**: Procesamiento automático con pdfplumber
3. **Agregar formación**: Opcionalmente sube PDFs de nuevos cursos/certificaciones
4. **Generar CV Maestro**: IA integra la nueva formación manteniendo tu experiencia
5. **Crear Perfil LinkedIn**: Genera contenido optimizado para LinkedIn
6. **CV Target**: Personaliza tu CV para un puesto específico
7. **Análisis ATS**: Evalúa compatibilidad con sistemas de filtrado automático
8. **Descargar PDF**: Exporta cualquier documento generado

### 📝 Opción 2: Crear CV desde Cero
1. **Formulario dinámico**: Completa tus datos personales
2. **Experiencia profesional**: Agrega hasta 10 empleos con fechas inteligentes
3. **Educación**: Incluye hasta 10 estudios con opción "En curso"
4. **Proyectos**: Destaca hasta 10 proyectos relevantes
5. **Habilidades**: Lista tus competencias técnicas y blandas
6. **Generación con IA**: Crea CV Maestro, LinkedIn y CV Target
7. **Análisis ATS**: Score y recomendaciones para optimizar tu CV
8. **Exportación PDF**: Descarga todos los documentos generados

### 🤖 Prompts Inteligentes
- **Prompt Maestro**: Integra nueva formación sin inventar experiencia
- **Prompt Target**: Personaliza CV sin alucinaciones, respetando la verdad
- **Prompt LinkedIn**: Genera perfil profesional optimizado
- **Prompt ATS**: Analiza compatibilidad con sistemas de reclutamiento
- **Anti-alucinaciones**: Reglas estrictas para mantener veracidad

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
- [x] Generación de CV Maestro con IA
- [x] Generación de Perfil LinkedIn optimizado
- [x] Generación de CV Target personalizado por puesto
- [x] Exportación a PDF de todos los documentos generados
- [x] Prompts ultra estrictos para evitar alucinaciones de IA
- [x] Validación avanzada de archivos PDF (tamaño, tipo, protección, contenido)
- [x] Diseño visual profesional de PDFs (tipografía, colores, iconos, layout)
- [x] Templates personalizables (Clásico, Moderno, Minimalista, Creativo)
- [x] Análisis ATS con scoring, palabras clave y recomendaciones

---

## 🧭 Roadmap / Próximos Pasos

- [x] Implementar extracción de texto con **pdfplumber**
- [x] Construir prompts avanzados (CV Maestro, Target y LinkedIn)
- [x] Integrar la API de IA (**OpenAI**)
- [x] Generar **CV Maestro** automáticamente
- [x] Generar **CV Target** según descripción de puesto
- [x] Generar **Perfil LinkedIn** optimizado
- [x] Exportar resultados descargables en **PDF**
- [x] Completar formulario de **CV desde cero** con campos dinámicos
- [x] Implementar campos de fecha con opción "Actualidad/En curso"
- [x] Validación avanzada de archivos PDF
- [x] Mejorar diseño visual de PDFs generados
- [x] Agregar templates de CV personalizables
- [x] Implementar análisis ATS del CV generado
- [ ] Mejorar estilo y diseño de la **UI de Streamlit**
- [ ] Deploy de la app en Streamlit Community Cloud
- [ ] Agregar soporte multiidioma

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
