# 🧪 CV Alchemist 2.0  
Aplicación web con IA desarrollada con **Streamlit** para crear, analizar y optimizar CVs.

---

## 📌 Descripción del Proyecto

CV Alchemist 2.0 es una aplicación interactiva que permite:

- Subir un CV en formato PDF para analizarlo y extraer su contenido.  
- Crear un CV desde cero mediante un formulario guiado.  
- Generar un **CV Maestro** y un **CV Optimizado** utilizando modelos de IA (integración pendiente).

El proyecto forma parte del módulo **Prompt Engineering** de CoderHouse y tiene como objetivo aplicar buenas prácticas de diseño de prompts en una aplicación funcional en Python.

---

## 📑 Presentación del Proyecto (PPT)

Para ver la presentación utilizada en la pre-entrega del curso, accedé aquí:

👉 [**Google Slides**](https://docs.google.com/presentation/d/1eEIGp8-rix1Tz2_vwm3lCRcLPKQTEXyUOgclLZ90vF0/edit?usp=sharing)

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.13**
- **Streamlit** (interfaz web)
- **PyPDF2 / pdfplumber** (extracción de texto — pendiente)
- **OpenAI API / Gemini API** (integración futura)
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
│   ├── extract_pdf.py            # Extracción de texto desde PDF (to-do)
│   ├── form_helpers.py           # Formulario para crear CV desde cero
│   ├── ai_service.py             # Integración futura con APIs de IA
│   ├── prompts.py                # Construcción de prompts maestro y target
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

## 🧱 Versión Anterior del Proyecto (MVP – Prompt Engineering I)

Este proyecto es una evolución de la primera versión del MVP desarrollada durante el curso Prompt Engineering I.

Podés ver el repositorio original aquí:  
👉 [cv-alchemist (MVP 2025)](https://github.com/vanerm/cv-alchemist)

La versión 2.0 incorpora nuevas funcionalidades, mejor arquitectura interna y un enfoque más completo para la creación y optimización de CVs utilizando IA.

---

## 🚧 Estado Actual del Proyecto

- [x] Estructura base funcionando  
- [x] Interfaz Streamlit operativa  
- [x] Carga de PDF funcional (sin extracción real aún)  
- [ ] Formulario “Crear CV desde cero” pendiente  
- [ ] Módulos de IA preparados pero no integrados  

---

## 🧭 Roadmap / Próximos Pasos

- [ ] Implementar extracción de texto con **pdfplumber**
- [ ] Validar archivo PDF (formato, permisos, extractabilidad)
- [ ] Manejo de errores en la extracción (mensajes claros al usuario)
- [ ] Normalizar y limpiar el texto extraído
- [ ] Guardar el contenido procesado en session_state
- [ ] Construir prompts avanzados (CV Maestro y CV Target)
- [ ] Integrar la API de IA (**OpenAI o Gemini**)
- [ ] Implementar funciones de IA en ai_service.py
- [ ] Generar **CV Maestro** automáticamente
- [ ] Generar **CV Target** según descripción de puesto
- [ ] Diseñar interfaz para mostrar CV generado y permitir descarga
- [ ] Exportar resultados descargables (**PDF / TXT**)
- [ ] Completar formulario de **CV desde cero**
- [ ] Unificar datos del PDF + formulario
- [ ] Mejorar estilo y diseño de la **UI de Streamlit**
- [ ] Deploy de la app en Streamlit Community Cloud (obtener URL pública .streamlit.app)
- [ ] Actualizar el README con el enlace a la app desplegada

---

## 🎓 Propósito Educativo

Este proyecto se desarrolla como parte del curso **Prompt Engineering para Programadores – CoderHouse**.

El objetivo principal es practicar:

**Diseño y optimización de prompts**
- **Integración de IA en aplicaciones reales**
- **Modularización limpia**
- **Creación rápida de interfaces funcionales con Streamlit**

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


