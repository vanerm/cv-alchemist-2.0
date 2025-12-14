# 🧪 CV Alchemist 2.0  
Aplicación web con IA desarrollada con **Streamlit** para crear, analizar y optimizar CVs.

## 🚀 Aplicación en Vivo

👉 **[Probar CV Alchemist 2.0](https://cv-alchemist.streamlit.app/)**

*La aplicación está desplegada en Streamlit Community Cloud y lista para usar.*

---

## 📌 Descripción del Proyecto

### 🎯 Problemática
En el contexto actual, los profesionales necesitan actualizar y adaptar sus CVs constantemente para mantenerse competitivos. Sin embargo, los CVs exportados desde LinkedIn suelen ser genéricos, difíciles de personalizar y poco optimizados para sistemas ATS.

Además, muchos usuarios no cuentan con un CV previo en PDF y requieren una alternativa guiada para generarlo desde cero.

Esta situación genera una necesidad clara: **automatizar la creación y optimización de CVs mediante IA**, reduciendo tiempo, errores y esfuerzo manual.

### 💡 Solución Propuesta
Se desarrolló una aplicación web completa en Streamlit llamada **CV Alchemist 2.0**, que ofrece un flujo integral de 6 pasos:

**🔄 Flujo de Entrada Dual:**
- **Subir un CV en PDF** (con validación avanzada y extracción inteligente), o
- **Completar un formulario guiado** para generar un CV base desde cero con validación en tiempo real

**📚 Enriquecimiento Opcional:**
- **Carga de formación adicional** mediante PDFs de cursos, certificaciones y planes de estudio
- **Integración automática** de nueva formación con experiencia existente

**🤖 Generación Inteligente con IA:**
A través de prompts diseñados con técnicas avanzadas de ingeniería y reglas anti-alucinaciones, la IA procesa la información y genera:

1. **CV Maestro actualizado** - Integra toda la información de forma coherente
2. **Perfil LinkedIn optimizado** - Contenido específico para redes profesionales
3. **CV Target personalizado** - Adaptado para ofertas laborales específicas

**🔍 Análisis y Optimización:**
- **Análisis ATS completo** con scoring 0-100 y recomendaciones accionables
- **Templates profesionales** personalizables según industria
- **Exportación en PDF** con diseño profesional

**🛡️ Características Avanzadas:**
- **Selección de modelos de IA** (OpenAI/Gemini) con fallback automático
- **Validación robusta** de datos y archivos
- **Interfaz responsive** con progreso en tiempo real

De esta forma, el flujo se vuelve accesible, completo y profesional para cualquier tipo de usuario.

---

**🎯 Resultado Final:**
Una plataforma completa de optimización de CVs que combina la flexibilidad de entrada (PDF o formulario), el poder de la IA generativa con múltiples modelos, y herramientas profesionales de análisis y exportación.

El proyecto forma parte del módulo **Prompt Engineering** de CoderHouse y demuestra la aplicación práctica de técnicas avanzadas de diseño de prompts, arquitectura modular y desarrollo de aplicaciones web con IA en Python.

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

## 💰 Justificación de la Viabilidad Técnica y Económica

- La aplicación se **desarrolló en Streamlit**, que facilita interfaces web sin necesidad de frameworks complejos
- La integración con modelos de IA se **realiza mediante llamadas a API** (Gemini u OpenAI)
- El costo es controlable: el flujo requiere **solo dos llamadas principales**, lo cual es económico
- Las librerías necesarias (PyPDF2, Streamlit, etc.) son gratuitas
- El proyecto **escaló de forma natural** desde una versión inicial hacia una aplicación web completa


### 🧭 Evolución desde el MVP Anterior

Este proyecto es una evolución de la primera versión desarrollada durante el curso **Prompt Engineering I** de CoderHouse.

👉 **[Ver repositorio original (MVP 2025)](https://github.com/vanerm/cv-alchemist)**

**Principales mejoras implementadas:**

- **Migración completada** del flujo del MVP en Colab a una aplicación web interactiva
- **Modularización completa** (servicios, prompts, extracción, utils)
- **Implementación exitosa** de carga y validación de PDF
- **Incorporación** de un formulario guiado para crear el CV si el usuario no tiene un PDF
- **Integración completa** con modelos de IA (OpenAI / Gemini)
- **Deploy exitoso** en Streamlit Community Cloud

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
│   ├── form_validators.py        # Validadores de formularios (email, teléfono, URLs)
│   ├── ai_service.py             # Integración con OpenAI y Gemini APIs
│   ├── prompts.py                # Prompts optimizados (Maestro, Target, LinkedIn)
│   ├── pdf_generator.py          # Generación de PDFs con ReportLab
│   ├── pdf_validator.py          # Validación de archivos PDF
│   ├── ats_analyzer.py           # Análisis de compatibilidad ATS
│   ├── cv_templates.py           # Templates personalizables de CV
│   ├── ui_styles.py              # Estilos CSS personalizados
│   ├── ui_components.py          # Componentes reutilizables de UI
│   ├── utils.py                  # Funciones auxiliares
│   └── __init__.py
│
├── tests/                        # Scripts de testing y debugging
│   ├── test_apis.py              # Prueba de conectividad con APIs
│   ├── test_memory.py            # Monitor de uso de RAM
│   ├── test_validation.py        # Prueba de validadores
│   ├── test_pdf_design.py        # Prueba de generación de PDFs
│   ├── memory_monitor.py         # Widget opcional de monitoreo
│   └── README.md                 # Documentación de tests
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

## 🧪 Recursos de Prueba

Para probar la aplicación, puedes usar estos archivos de ejemplo:

- 📁 [CVs de ejemplo (Google Drive)](https://drive.google.com/drive/folders/1LQL5kqim86RRGkrAQSE_xxzHgKDc4QdO?usp=sharing)
- 📁 [Planes de estudio de ejemplo (Google Drive)](https://drive.google.com/drive/folders/13868l7n-mJJ_vfZD8g5x_RYOXDjJVQoa?usp=sharing)

**Cómo usar:**
1. Descarga un CV de ejemplo de la primera carpeta
2. Súbelo en la opción "Subir un CV existente (PDF)"
3. Opcionalmente, descarga un plan de estudios de la segunda carpeta
4. Agrégalo en el paso 2 para ver cómo la IA integra nueva formación

---

## ✨ Funcionalidades Principales

### 🔄 Flujo Unificado (Ambas Opciones)
Ambas opciones siguen la misma estructura de 6 pasos:

1. **Paso 1**: Subir CV existente (PDF) O Completar formulario manual
2. **Paso 2**: Agregar formación adicional (opcional) - PDFs de cursos/certificaciones
3. **Paso 3**: Generar CV Maestro con IA (integra datos + formación)
4. **Paso 4**: Crear Perfil LinkedIn optimizado
5. **Paso 5**: Generar CV Target personalizado para un puesto
6. **Paso 6**: Análisis ATS con scoring y recomendaciones

### 📄 Opción 1: Subir CV Existente
- **Carga de PDF**: Sube tu CV actual en formato PDF con validación avanzada
- **Extracción de texto**: Procesamiento automático con pdfplumber
- **Validación robusta**: Tamaño, tipo, protección y contenido legible
- **Metadata**: Información detallada del PDF procesado

### 📝 Opción 2: Crear CV desde Cero
- **Formulario dinámico**: Completa tus datos personales con validación en tiempo real
- **Experiencia profesional**: Agrega hasta 10 empleos con fechas inteligentes
- **Educación**: Incluye hasta 10 estudios con opción "En curso"
- **Proyectos**: Destaca hasta 10 proyectos relevantes con enlaces
- **Habilidades**: Lista tus competencias técnicas y blandas
- **Validación de datos**: Regex para email, teléfono, URLs y sanitización de texto
- **Selectores inteligentes**: Países y ciudades predefinidas para Latinoamérica y España

### 🆕 Características Comunes (Ambas Opciones)
- **Agregar formación**: Sube PDFs de cursos/certificaciones (opcional)
- **Generación con IA**: CV Maestro integrando toda la información
- **Perfil LinkedIn**: Contenido optimizado para redes profesionales
- **CV Target**: Personalización para puestos específicos
- **Análisis ATS**: Score 0-100 con recomendaciones accionables
- **Exportación PDF**: Descarga con templates profesionales personalizables

### 📚 Sistema de Carga de Formación Adicional
- **Carga múltiple de PDFs**: Sube planes de estudio, certificaciones y cursos
- **Extracción inteligente**: Procesamiento automático del contenido de formación
- **Integración con CV base**: La IA combina la nueva formación con tu experiencia existente
- **Validación de contenido**: Verificación de que los PDFs contienen información relevante
- **Procesamiento contextual**: Mantiene coherencia entre formación previa y nueva

### 🤖 Sistema de Selección de Modelo de IA
- **Selector inteligente en sidebar**: 
  - Opción OpenAI con múltiples modelos disponibles
  - Opción Gemini con modelos de última generación
  - Modo Auto con fallback inteligente
- **Modelos OpenAI disponibles**: 
  - gpt-4o-mini (rápido y económico)
  - gpt-4o (balance rendimiento/costo)
  - gpt-4-turbo-preview (máxima capacidad)
  - gpt-3.5-turbo (alternativa rápida)
- **Modelos Gemini disponibles**: 
  - gemini-flash-latest (velocidad optimizada)
  - gemini-2.5-flash (nueva generación rápida)
  - gemini-2.5-pro (máxima calidad)
  - gemini-pro-latest (versión más reciente)
- **Sistema de fallback robusto**: 
  - Si OpenAI falla por límites o errores, cambia automáticamente a Gemini
  - Manejo inteligente de errores de API
  - Continuidad del flujo sin intervención del usuario
- **Feedback dinámico en tiempo real**: 
  - Spinners que muestran el modelo específico en uso
  - Mensajes de estado durante el procesamiento
  - Notificaciones de cambio de modelo por fallback
- **Sistema de logging avanzado**: 
  - Seguimiento detallado en consola para debugging
  - Monitoreo de rendimiento por modelo
  - Registro de errores y fallbacks para optimización

### 🎨 Templates Profesionales
- **Clásico**: Formato tradicional con máxima compatibilidad ATS (⭐⭐⭐⭐⭐)
  - Ideal para: Legal, Finanzas, Consultoría, Gobierno
  - Características: Tipografía conservadora, estructura lineal, sin elementos gráficos
- **Moderno**: Balance perfecto entre diseño y parseabilidad (ATS ⭐⭐⭐⭐)
  - Ideal para: Tech, Startups, Ingeniería, Data Science
  - Características: Tipografía moderna, colores sutiles, iconos minimalistas
- **Minimalista**: Espaciado generoso y limpieza visual (ATS ⭐⭐⭐⭐)
  - Ideal para: Diseño, UX/UI, Arquitectura, Creatividad
  - Características: Mucho espacio en blanco, tipografía elegante, estructura clara
- **Creativo**: Más visual y diferenciado (ATS ⭐⭐⭐)
  - Ideal para: Marketing, Publicidad, Arte, Medios
  - Características: Colores vibrantes, elementos gráficos, layout innovador
- **Personalización completa**: 
  - Tipografía: Selección de fuentes profesionales
  - Colores: Paleta personalizable por template
  - Iconos: Biblioteca de iconos profesionales
  - Layout: Estructura adaptable según contenido

### 🔍 Análisis ATS Avanzado
- **Scoring 0-100**: Evaluación cuantitativa de compatibilidad con sistemas ATS
- **4 Criterios ponderados**: 
  - Formato y estructura (25%): Parseabilidad y organización
  - Palabras clave (40%): Coincidencia con términos del puesto
  - Contenido y claridad (20%): Legibilidad y coherencia
  - Optimización ATS (15%): Elementos técnicos de compatibilidad
- **Análisis de palabras clave**: Identificación de términos encontrados vs faltantes
- **Fortalezas y debilidades**: Evaluación detallada por cada criterio
- **Recomendaciones accionables**: Sugerencias específicas y priorizadas para mejorar
- **Detalles expandibles**: Información completa por cada métrica evaluada
- **Comparación con estándares**: Benchmarking contra mejores prácticas ATS

### 🤖 Sistema de Prompts Inteligentes
- **Prompt Maestro avanzado**: 
  - Integra nueva formación respetando experiencia existente
  - Evita inventar experiencias o habilidades no mencionadas
  - Mantiene coherencia temporal y profesional
  - Optimiza estructura y redacción sin alterar hechos
- **Prompt Target especializado**: 
  - Personaliza CV para puestos específicos sin alucinaciones
  - Resalta experiencia relevante sin inventar nueva
  - Adapta lenguaje y énfasis según la descripción del puesto
  - Mantiene veracidad absoluta de la información original
- **Prompt LinkedIn profesional**: 
  - Genera contenido optimizado para redes profesionales
  - Adapta tono y formato para plataforma LinkedIn
  - Crea resumen ejecutivo atractivo y profesional
  - Optimiza para búsquedas y networking
- **Prompt ATS especializado**: 
  - Analiza compatibilidad con sistemas de reclutamiento
  - Evalúa criterios técnicos y de contenido
  - Genera recomendaciones accionables y priorizadas
  - Proporciona scoring detallado y justificado
- **Sistema anti-alucinaciones robusto**: 
  - Reglas estrictas para mantener veracidad de la información
  - Validación cruzada de datos generados
  - Prohibición explícita de inventar experiencias
  - Monitoreo de consistencia en todas las generaciones

### 🛡️ Seguridad y Validación Robusta
- **Validación de formularios en tiempo real**: 
  - Email: Regex estricto para formato válido con @ y dominio
  - Teléfono: Solo números, +, -, ( ) con longitud mínima/máxima
  - URLs: Verificación de formato http/https con dominio válido
  - Nombres: Solo letras, espacios, acentos, apóstrofes y guiones
- **Sanitización avanzada de inputs**: 
  - Remoción de caracteres de control y potencialmente peligrosos
  - Prevención de inyección de código en campos de texto
  - Normalización de caracteres especiales y acentos
- **Validación exhaustiva de PDFs**: 
  - Verificación de tamaño (límite de 200MB)
  - Validación de tipo de archivo y extensión
  - Detección de PDFs protegidos con contraseña
  - Verificación de contenido legible y extracción exitosa
- **Sistema de feedback detallado**: 
  - Mensajes de error específicos para cada tipo de validación
  - Sugerencias de corrección para errores comunes
  - Indicadores visuales de campos válidos/inválidos

### 🎨 Interfaz de Usuario Avanzada
- **Sidebar interactivo dinámico**: 
  - Progreso en tiempo real con indicadores visuales
  - Estadísticas de documentos generados y score ATS
  - Selección de modelo de IA con fallback automático
  - Enlaces rápidos a documentación y recursos
- **Sistema de temas profesional**: 
  - Tema lila pastel consistente en toda la aplicación
  - Configuración de tema dark forzado para mejor experiencia
  - Gradientes y sombras para profundidad visual
- **Indicadores de progreso inteligentes**: 
  - Checkmarks verdes para pasos completados
  - Indicador especial para pasos opcionales omitidos
  - Barra de progreso visual por etapas
- **Gestión de sesión**: 
  - Botón reiniciar que limpia sesión sin recargar página
  - Persistencia de datos durante la sesión
  - Manejo inteligente de estados de la aplicación
- **Sistema de mensajes contextuales**: 
  - Alertas de success, info, warning y error con iconos
  - Spinners dinámicos que muestran el modelo de IA en uso
  - Feedback inmediato para todas las acciones del usuario
- **Diseño responsive**: 
  - Adaptable a diferentes tamaños de pantalla
  - Optimizado para desktop y mobile
  - Componentes que se reorganizan según el espacio disponible

---

## 🧱 Versión Anterior del Proyecto (MVP – Prompt Engineering I)

Este proyecto es una evolución de la primera versión del MVP desarrollada durante el curso Prompt Engineering I.

Podés ver el repositorio original aquí:  
👉 [cv-alchemist (MVP 2025)](https://github.com/vanerm/cv-alchemist)

La versión 2.0 incorpora nuevas funcionalidades, mejor arquitectura interna y un enfoque más completo para la creación y optimización de CVs utilizando IA.

---

## ✅ Estado Actual del Proyecto

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
- [x] Scripts de testing y debugging organizados en carpeta tests/
- [x] Monitoreo de uso de RAM (183 MB máximo - óptimo para deploy)
- [x] Deploy en Streamlit Community Cloud

---

## 🚀 Ideas para Futuras Versiones

*El proyecto actual está completo y funcional. Estas son posibles mejoras para versiones futuras:*

- 🌍 **Soporte multidioma**: Interfaz y generación en inglés y portugués
- 📁 **Historial de documentos**: Guardar y gestionar CVs generados anteriormente
- 📄 **Exportación Word**: Descarga en formato .docx además de PDF
- 🤖 **Más modelos de IA**: Integración con Claude, Llama y otros LLMs
- 📈 **Análisis comparativo**: Comparar múltiples versiones de CV
- 🔗 **Integración job boards**: Conexión directa con portales de empleo
- 🎨 **Editor visual**: Personalización avanzada de templates en tiempo real
- 📊 **Dashboard analytics**: Métricas de rendimiento y uso de la aplicación

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
