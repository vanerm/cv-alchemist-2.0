# Changelog - CV Alchemist 2.0

## [Unreleased] - 2024-12-07

### ✨ Added
- **Diseño visual profesional de PDFs** con 4 fases implementadas:
  1. Tipografía y espaciado mejorado (jerarquía visual clara)
  2. Colores profesionales y líneas divisorias (paleta azul + grises)
  3. Iconos simples con Pillow (bullets personalizados)
  4. Layout optimizado con Platypus (estructura profesional)

- **Validación avanzada de archivos PDF** con 6 validaciones implementadas:
  1. Validación de tamaño de archivo (máx 10MB)
  2. Validación de tipo de archivo real (header `%PDF-`)
  3. Detección de PDFs protegidos con contraseña
  4. Detección de PDFs corruptos o dañados
  5. Validación de contenido extraíble (detección de PDFs escaneados)
  6. Feedback visual con metadata (páginas, caracteres, tamaño)

- Nuevo módulo `src/pdf_validator.py` con clase `PDFValidationResult`
- Script de pruebas `test_validation.py`
- Documentación completa en `docs/PDF_VALIDATION.md`
- Documentación de mejoras de diseño en `docs/PDF_DESIGN_IMPROVEMENTS.md`
- Dependencia `Pillow` para procesamiento de imágenes e iconos

### 🔧 Changed
- `src/pdf_generator.py`: Reescrito completamente con diseño profesional de 4 fases
- `src/extract_pdf.py`: Funciones ahora retornan tuplas con texto y resultado de validación
- `app.py`: Función `process_uploaded_pdfs()` integra validaciones y muestra feedback detallado
- `requirements.txt`: Agregada dependencia `Pillow`
- `README.md`: Marcadas tareas de validación y diseño visual como completadas

### 🐛 Fixed
- Ordenamiento alfabético de países y ciudades en selectboxes
- Error `UnboundLocalError` al usar variables `paises` y `ciudades_por_pais` antes de definirlas
- Error `ValueError` en generación de PDF por caracteres especiales mal escapados

### 📝 Documentation
- Agregado `CHANGELOG.md` para tracking de cambios
- Agregado `docs/PDF_VALIDATION.md` con documentación técnica completa

---

## [Previous] - 2024-12-06

### ✨ Added
- Exportación a PDF de CV Maestro, LinkedIn y CV Target con ReportLab
- Selectboxes de país y ciudad con 15 países latinoamericanos
- Campos de fecha con `st.date_input` y checkbox "Actualidad/En curso"
- Formulario dinámico "Crear CV desde cero" con hasta 10 entradas por sección
- Prompts ultra estrictos anti-alucinaciones

### 🔧 Changed
- Removido `st.form()` para permitir actualización dinámica de UI
- Aumentado límite de entradas de 3 a 10 para empleos, educación y proyectos

---

## [Initial] - 2024-12-05

### ✨ Added
- Estructura base del proyecto
- Integración con OpenAI API
- Extracción de texto desde PDF con pdfplumber
- Generación de CV Maestro, LinkedIn Profile y CV Target
- Interfaz Streamlit con dos flujos principales
