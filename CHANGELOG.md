# Changelog - CV Alchemist 2.0

## [Unreleased] - 2025

### ✨ Added - Análisis ATS
- **Nuevo módulo `ats_analyzer.py`**: Sistema completo de análisis de compatibilidad ATS
- **Prompt especializado**: Evaluación con IA de 4 criterios principales (Formato, Palabras Clave, Contenido, Optimización)
- **Scoring 0-100**: Métrica clara de compatibilidad con sistemas de reclutamiento
- **Análisis de palabras clave**: Identificación de términos encontrados vs faltantes
- **Recomendaciones accionables**: Sugerencias específicas para mejorar el CV
- **Integración en UI**: Sección de análisis ATS después de generar CV Target
- **Visualización completa**: Score, nivel, fortalezas, debilidades, palabras clave y recomendaciones
- **Documentación ATS**: Guía completa en `docs/ATS_ANALYSIS.md`

### 🎨 Added - Templates Personalizables
- **Nuevo módulo `cv_templates.py`**: Sistema de templates con configuración visual
- **4 templates profesionales**:
  - Clásico: Formal y tradicional (máxima compatibilidad ATS)
  - Moderno: Profesional y actual (tech/startups)
  - Minimalista: Limpio y espacioso (diseño/UX)
  - Creativo: Vibrante y llamativo (marketing/publicidad)
- **Selector de templates**: UI para elegir estilo en cada exportación PDF
- **Configuración por template**: Colores, fuentes, tamaños, espaciado, divisores

### 🔧 Modified
- **app.py**: Integración de análisis ATS en ambos flujos (subir CV y crear desde cero)
- **README.md**: Actualización con nueva funcionalidad ATS y templates
- **Estructura del proyecto**: Nuevos módulos documentados

### 📚 Documentation
- **ATS_ANALYSIS.md**: Guía completa sobre análisis ATS
  - Explicación de criterios de evaluación
  - Interpretación de scores
  - Mejores prácticas y casos de uso
  - FAQ y recursos adicionales

---

## [2.0.0] - 2025-01

### ✨ Added
- Formulario dinámico "Crear CV desde cero"
- Campos de fecha inteligentes con opción "Actualidad/En curso"
- Generación de CV Maestro con IA
- Generación de Perfil LinkedIn optimizado
- Generación de CV Target personalizado
- Exportación a PDF de todos los documentos
- Validación avanzada de archivos PDF (6 capas de seguridad)
- Diseño visual profesional de PDFs (tipografía, colores, iconos)
- Prompts ultra estrictos anti-alucinaciones

### 🔧 Modified
- Refactorización de `build_prompt_targeted`
- Mejora de extracción de texto con pdfplumber
- Optimización de generación de PDFs con ReportLab

---

## [1.0.0] - 2024

### ✨ Initial Release
- Estructura base del proyecto
- Interfaz Streamlit operativa
- Extracción de texto desde PDF
- Integración con OpenAI API
- Prompts básicos para CV Maestro y Target
