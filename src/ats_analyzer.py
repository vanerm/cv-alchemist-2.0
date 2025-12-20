# src/ats_analyzer.py

"""
Módulo de análisis ATS (Applicant Tracking System).

Analiza un CV generado y proporciona:
- Score de compatibilidad ATS (0-100)
- Palabras clave encontradas vs esperadas
- Recomendaciones específicas de mejora
"""

import re
from typing import Dict, List, Tuple
from .ai_service import generate_cv_output


def analyze_ats_compatibility(cv_content: str, job_description: str = "") -> Dict:
    """
    Analiza la compatibilidad ATS de un CV.
    
    Args:
        cv_content: Contenido del CV a analizar
        job_description: Descripción del puesto (opcional, mejora el análisis)
    
    Returns:
        Dict con: score, keywords_found, keywords_missing, recommendations, details
    """
    
    # Construir prompt de análisis ATS
    prompt = _build_ats_analysis_prompt(cv_content, job_description)
    
    # Llamar a la IA para análisis
    analysis_text = generate_cv_output(prompt)
    
    # Parsear respuesta
    result = _parse_ats_analysis(analysis_text)
    
    return result


def _detect_entry_level_position(job_description: str) -> bool:
    """Detecta si es un puesto entry-level/sin experiencia requerida."""
    if not job_description:
        return False
    
    job_lower = job_description.lower()
    
    entry_level_keywords = [
        # Español
        "pasante", "pasantía", "trainee", "practicante", "sin experiencia",
        "entry level", "nivel inicial", "recién graduado", "primer empleo",
        "estudiante", "aprendiz", "junior", "jr", "graduate program",
        "sin experiencia previa", "no requiere experiencia", "0 años",
        "0-1 años", "recien egresado", "egresado",
        
        # Inglés (común en tech)
        "intern", "internship", "entry-level", "no experience required",
        "recent graduate", "new grad", "apprentice", "trainee program",
        "0 years", "0-1 years", "fresh graduate"
    ]
    
    return any(keyword in job_lower for keyword in entry_level_keywords)


def _build_ats_analysis_prompt(cv_content: str, job_description: str) -> str:
    """Construye el prompt para análisis ATS."""
    
    # Detectar si es puesto entry-level
    is_entry_level = _detect_entry_level_position(job_description)
    
    job_section = ""
    if job_description.strip():
        job_section = f"""
--- DESCRIPCIÓN DEL PUESTO ---
{job_description}
--- FIN DESCRIPCIÓN ---
"""
    
    # Ajustar criterios según tipo de puesto
    if is_entry_level:
        criteria_weights = """
**CRITERIOS PARA PUESTO ENTRY-LEVEL/SIN EXPERIENCIA (pesos ajustados):**

**1. EDUCACIÓN Y FORMACIÓN (35 puntos)**
- ¿Tiene educación formal relevante al puesto?
- ¿Incluye cursos, certificaciones o formación adicional?
- ¿La formación está actualizada y es pertinente?

**2. PROYECTOS Y HABILIDADES (30 puntos)**
- ¿Incluye proyectos académicos, personales o de práctica?
- ¿Las habilidades técnicas coinciden con los requisitos?
- ¿Demuestra conocimiento práctico aunque sea teórico?

**3. PALABRAS CLAVE (25 puntos)**
- ¿Contiene tecnologías, herramientas o conceptos del puesto?
- ¿Menciona habilidades blandas relevantes?

**4. FORMATO Y ESTRUCTURA (10 puntos)**
- ¿Tiene secciones claramente identificadas?
- ¿Es fácil de leer y parsear por ATS?

NOTA: Para puestos entry-level, NO se penaliza la falta de experiencia laboral.
Se valora potencial, formación y proyectos académicos/personales.
"""
    else:
        criteria_weights = """
**CRITERIOS PARA PUESTO CON EXPERIENCIA REQUERIDA (pesos estándar):**

**1. EXPERIENCIA PROFESIONAL (40 puntos)**
- ¿Tiene experiencia laboral relevante al puesto?
- ¿Los logros están cuantificados y son específicos?
- ¿La progresión profesional es coherente?

**2. PALABRAS CLAVE (30 puntos)**
- ¿Contiene palabras clave relevantes de la descripción del puesto?
- ¿Las palabras clave aparecen en contexto apropiado?

**3. FORMATO Y ESTRUCTURA (20 puntos)**
- ¿Tiene secciones claramente identificadas?
- ¿Evita elementos complejos que dificulten el parseo ATS?

**4. EDUCACIÓN Y FORMACIÓN (10 puntos)**
- ¿La educación es relevante y está actualizada?
- ¿Incluye certificaciones pertinentes?
"""
    
    prompt = f"""
Actúa como un experto en sistemas ATS (Applicant Tracking Systems) y reclutamiento.

Tu tarea es analizar el siguiente CV y evaluar su compatibilidad con sistemas ATS.

{job_section}

--- INICIO DEL CV ---
{cv_content}
--- FIN DEL CV ---

DETECCIÓN AUTOMÁTICA: {'Este es un PUESTO ENTRY-LEVEL/SIN EXPERIENCIA REQUERIDA' if is_entry_level else 'Este es un PUESTO CON EXPERIENCIA REQUERIDA'}

VALIDACIÓN PREVIA OBLIGATORIA:
Antes de evaluar, verifica si el CV contiene información sustancial.
Si el CV SOLO tiene datos de contacto (nombre, email) SIN NINGUNA sección con contenido
(ni experiencia, ni educación, ni proyectos, ni habilidades, ni resumen), asigna automáticamente:
- SCORE_ATS: 15
- NIVEL: Crítico
- Incluye en DEBILIDADES: "CV prácticamente vacío - falta experiencia, educación y proyectos"
- Incluye en RECOMENDACIONES: "Completar todas las secciones con información detallada antes de postular"

{criteria_weights}

Debes evaluar los criterios correspondientes y proporcionar un análisis detallado:

**1. FORMATO Y ESTRUCTURA (25 puntos)**
- ¿Tiene secciones claramente identificadas? (Experiencia, Educación, Habilidades)
- ¿Usa encabezados estándar reconocibles por ATS?
- ¿La estructura es limpia y sin elementos complejos?
- ¿Evita tablas, columnas múltiples, gráficos o imágenes?

**2. PALABRAS CLAVE (40 puntos)**
{"- ¿Contiene palabras clave relevantes de la descripción del puesto?" if job_description else "- ¿Contiene palabras clave técnicas y profesionales relevantes?"}
- ¿Las palabras clave aparecen en contexto apropiado?
- ¿Hay suficiente densidad de términos técnicos sin keyword stuffing?
{"- ¿Coincide con los requisitos técnicos del puesto?" if job_description else ""}

**IMPORTANTE PARA PALABRAS CLAVE:**
- Si el CV tiene contenido insuficiente, no evalúes palabras clave detalladamente
- Para puestos ENTRY-LEVEL: acepta palabras clave en educación, proyectos y habilidades con igual peso
- Para puestos CON EXPERIENCIA: prioriza palabras clave en experiencia laboral
- Para CVs con contenido adecuado:
  - Considera TODAS las variaciones y acrónimos comunes de términos técnicos
  - Ejemplos de equivalencias: palabra completa = minúsculas = acrónimo = traducción
  - Busca la palabra en TODO el CV (experiencia, proyectos, habilidades, educación)
  - Si encuentras el acrónimo de una palabra, considera que la palabra completa SÍ está presente
  - Si una palabra aparece en CUALQUIER sección del CV, NO la marques como faltante
  - Solo marca como faltante si ni la palabra completa NI su acrónimo aparecen en el CV

**3. CONTENIDO Y CLARIDAD (20 puntos)**
- ¿La experiencia está bien descrita con logros cuantificables?
- ¿Las fechas están en formato estándar?
- ¿La información de contacto es clara y completa?
- ¿El CV tiene longitud apropiada (1-2 páginas)?

**4. OPTIMIZACIÓN ATS (15 puntos)**
- ¿Usa verbos de acción al inicio de las descripciones?
- ¿Evita abreviaturas no estándar?
- ¿Incluye tanto acrónimos como términos completos cuando corresponde?
- ¿Las habilidades están listadas claramente?

FORMATO DE RESPUESTA OBLIGATORIO:

**SCORE_ATS:** [número entre 0-100]

**NIVEL:** [Excelente / Bueno / Aceptable / Necesita Mejoras / Crítico]

**PALABRAS_CLAVE_ENCONTRADAS:**
- palabra1
- palabra2
- palabra3

**PALABRAS_CLAVE_FALTANTES:**
- palabra1 (sugerencia: agregar en experiencia/proyectos con ejemplo concreto)
- palabra2 (sugerencia: agregar en experiencia/proyectos con ejemplo concreto)

NOTAS IMPORTANTES:
1. Solo incluye palabras que NO aparecen en el CV (ni como palabra completa ni como acrónimo)
2. Si la palabra está en habilidades pero NO en experiencia/proyectos, NO la marques como faltante
3. En su lugar, menciona en RECOMENDACIONES que sería mejor incluir ejemplos prácticos de uso
4. Si encuentras el acrónimo de una palabra clave en cualquier parte del CV, NO la marques como faltante

**FORTALEZAS:**
- Fortaleza 1
- Fortaleza 2

**DEBILIDADES:**
- Debilidad 1
- Debilidad 2

**RECOMENDACIONES:**
1. Recomendación específica y accionable
2. Recomendación específica y accionable
3. Recomendación específica y accionable

**DETALLES_POR_CRITERIO:**
- Formato y Estructura: [X/25] - breve comentario
- Palabras Clave: [X/40] - breve comentario
- Contenido y Claridad: [X/20] - breve comentario
- Optimización ATS: [X/15] - breve comentario

Sé específico, objetivo y proporciona recomendaciones accionables.
"""
    
    return prompt.strip()


def _parse_ats_analysis(analysis_text: str) -> Dict:
    """
    Parsea el texto de análisis de la IA y extrae información estructurada.
    """
    
    result = {
        "score": 0,
        "level": "Desconocido",
        "keywords_found": [],
        "keywords_missing": [],
        "strengths": [],
        "weaknesses": [],
        "recommendations": [],
        "details": {},
        "raw_analysis": analysis_text
    }
    
    # Extraer score
    score_match = re.search(r'\*\*SCORE_ATS:\*\*\s*(\d+)', analysis_text)
    if score_match:
        result["score"] = int(score_match.group(1))
    
    # Extraer nivel
    level_match = re.search(r'\*\*NIVEL:\*\*\s*([^\n]+)', analysis_text)
    if level_match:
        result["level"] = level_match.group(1).strip()
    
    # Extraer palabras clave encontradas
    kw_found_section = re.search(
        r'\*\*PALABRAS_CLAVE_ENCONTRADAS:\*\*\s*((?:- [^\n]+\n?)+)',
        analysis_text
    )
    if kw_found_section:
        keywords = re.findall(r'- ([^\n]+)', kw_found_section.group(1))
        result["keywords_found"] = [kw.strip() for kw in keywords]
    
    # Extraer palabras clave faltantes
    kw_missing_section = re.search(
        r'\*\*PALABRAS_CLAVE_FALTANTES:\*\*\s*((?:- [^\n]+\n?)+)',
        analysis_text
    )
    if kw_missing_section:
        keywords = re.findall(r'- ([^\n]+)', kw_missing_section.group(1))
        result["keywords_missing"] = [kw.strip() for kw in keywords]
    
    # Extraer fortalezas
    strengths_section = re.search(
        r'\*\*FORTALEZAS:\*\*\s*((?:- [^\n]+\n?)+)',
        analysis_text
    )
    if strengths_section:
        strengths = re.findall(r'- ([^\n]+)', strengths_section.group(1))
        result["strengths"] = [s.strip() for s in strengths]
    
    # Extraer debilidades
    weaknesses_section = re.search(
        r'\*\*DEBILIDADES:\*\*\s*((?:- [^\n]+\n?)+)',
        analysis_text
    )
    if weaknesses_section:
        weaknesses = re.findall(r'- ([^\n]+)', weaknesses_section.group(1))
        result["weaknesses"] = [w.strip() for w in weaknesses]
    
    # Extraer recomendaciones
    recommendations_section = re.search(
        r'\*\*RECOMENDACIONES:\*\*\s*((?:\d+\. [^\n]+\n?)+)',
        analysis_text
    )
    if recommendations_section:
        recommendations = re.findall(r'\d+\. ([^\n]+)', recommendations_section.group(1))
        result["recommendations"] = [r.strip() for r in recommendations]
    
    # Extraer detalles por criterio
    details_section = re.search(
        r'\*\*DETALLES_POR_CRITERIO:\*\*\s*((?:- [^\n]+\n?)+)',
        analysis_text
    )
    if details_section:
        details_lines = re.findall(r'- ([^\n]+)', details_section.group(1))
        for line in details_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result["details"][key.strip()] = value.strip()
    
    return result


def get_score_color(score: int) -> str:
    """Retorna el color apropiado según el score ATS."""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"


def get_score_emoji(score: int) -> str:
    """Retorna el emoji apropiado según el score ATS."""
    if score >= 80:
        return "✅"
    elif score >= 60:
        return "⚠️"
    else:
        return "❌"
