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

## 🚧 Estado Actual del Proyecto

- [x] Estructura base funcionando  
- [x] Interfaz Streamlit operativa  
- [x] Carga de PDF funcional (sin extracción real aún)  
- [ ] Formulario “Crear CV desde cero” pendiente  
- [ ] Módulos de IA preparados pero no integrados  

---

## 🧭 Roadmap / Próximos Pasos

- [ ] Implementar extracción de texto con **pdfplumber**
- [ ] Normalizar y limpiar el texto extraído
- [ ] Construir prompts avanzados
- [ ] Integrar la API de IA (**OpenAI o Gemini**)
- [ ] Generar **CV Maestro** automáticamente
- [ ] Generar **CV Target** según descripción de puesto
- [ ] Exportar resultados descargables (**PDF / TXT**)
- [ ] Completar formulario de **CV desde cero**
- [ ] Mejorar estilo y diseño de la **UI de Streamlit**
- [ ] Deploy de la app en Streamlit Community Cloud (obtener URL pública .streamlit.app)
- [ ] Actualizar el README con el enlace a la app desplegada

---

## 🎓 Propósito Educativo

Este proyecto se desarrolla como parte del curso **Prompt Engineering para Programadores – CoderHouse**.

El objetivo principal es practicar:

- **Diseño y optimización de prompts**
- • **Integración de IA en aplicaciones reales**
- • **Modularización limpia**
- • **Creación rápida de interfaces funcionales con Streamlit**

---

## 📄 Licencia
El proyecto está disponible bajo la licencia MIT, permitiendo su uso libre para fines personales, académicos o experimentales.
Para más detalles, consulta el archivo LICENSE.

---
## 👋 About Me

Soy Vanesa Mizrahi, desarrolladora móvil iOS y analista de datos.
Me especializo en:

- Desarrollo móvil iOS  
- Ciencia de Datos aplicada a negocio
- Modelos interpretables
- Integración con APIs externas

### 🔗 Conecta conmigo
- **LinkedIn:** [Vanesa Mizrahi](https://www.linkedin.com/in/vanesamizrahi)


