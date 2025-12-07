# src/prompts.py
from textwrap import dedent


def build_prompt_master(cv_text: str, new_studies: str) -> str:
    """
    Construye el prompt para generar el CV Maestro actualizado.
    El lector debe pasar:
    - cv_text: texto del CV base (extraído del PDF o creado desde cero).
    - new_studies: texto descriptivo de la nueva formación / plan de estudios.
    """
    prompt = f"""
    Actúa como un experto redactor de CVs y orientador profesional de alto nivel.

    Tu tarea es analizar dos documentos: el CV base de un candidato y el contenido
    de un nuevo programa de estudios que ha completado.

    Tu misión es crear una nueva versión del CV, un "CV Maestro", que integre de forma
    profesional y coherente la nueva formación.

    Indicaciones clave:
    - No te limites a añadir una sección nueva.
    - Si es necesario, reestructura el CV completo.
    - Mejora la redacción del resumen profesional para reflejar las nuevas habilidades.
    - Asegúrate de que el resultado sea un documento pulido, profesional y actualizado.
    - Mantén un tono profesional, claro y directo.
    - Respeta los datos reales del candidato; no inventes información.

    A continuación se incluyen los documentos:

    --- INICIO DEL CV BASE ---
    {cv_text}
    --- FIN DEL CV BASE ---

    --- INICIO DEL PROGRAMA DE ESTUDIOS ---
    {new_studies}
    --- FIN DEL PROGRAMA DE ESTUDIOS ---

    Devuelve únicamente el texto completo del CV maestro actualizado,
    listo para copiar y pegar en una plantilla de CV.
    No añadas comentarios, explicaciones ni encabezados adicionales.
    El formato puede ser texto plano con secciones claramente diferenciadas.
    """
    return dedent(prompt).strip()


def build_prompt_targeted(master_cv: str, job_description: str) -> str:
    """
    Construye el prompt para generar un CV optimizado para un puesto específico.
    El lector debe pasar:
    - master_cv: texto del CV Maestro actualizado.
    - job_description: descripción del puesto objetivo (idealmente ya estructurada).
    """
    prompt = f"""
    Actúa como un Career Coach y experto en reclutamiento técnico,
    especializado en optimizar CVs para pasar filtros ATS y destacar
    ante managers de contratación.

    Tu proceso de pensamiento interno debe seguir estas etapas (NO las imprimas,
    solo utilízalas como guía):

    1) Análisis del candidato:
       - Analiza el "CV Maestro" y determina el nivel aproximado de seniority
         (Junior, Semi-Senior o Senior) en su campo principal.
       - Identifica si el puesto objetivo está alineado con su experiencia previa
         o si se trata de una transición de carrera hacia un nuevo campo.

    2) Definición de estrategia:
       - Si se trata de una transición de carrera:
         * Enfatiza la formación reciente, proyectos relevantes y habilidades
           transferibles.
         * No presentes la formación o proyectos como experiencia laboral
           profesional si no lo son.
       - Si el rol está alineado con la experiencia previa:
         * Alinea de forma directa la experiencia pasada con los requisitos del puesto.
         * Destaca logros, métricas y tecnologías relevantes.

    3) Optimización para ATS:
       - Integra de forma natural las palabras clave y tecnologías mencionadas
         en la descripción del puesto (hard skills y soft skills).
       - Refuerza el resumen profesional, la sección de experiencia y la sección
         de habilidades para que reflejen el encaje con el rol.

    Reglas críticas:
    - No inventes experiencia ni títulos que no estén en el CV Maestro.
    - Puedes reordenar, resumir o reescribir, pero siempre basado en la información dada.
    - Mantén un tono profesional, honesto y claro.
    - El resultado debe ser un CV que la persona pueda usar tal cual para postularse.

    Documentos para tu análisis:

    --- INICIO DEL CV MAESTRO ---
    {master_cv}
    --- FIN DEL CV MAESTRO ---

    --- INICIO DE LA DESCRIPCIÓN DEL PUESTO ---
    {job_description}
    --- FIN DE LA DESCRIPCIÓN DEL PUESTO ---

    Devuelve únicamente el texto del CV optimizado, listo para ser copiado y pegado
    en una plantilla de diseño profesional. No incluyas comentarios, explicaciones
    ni encabezados adicionales fuera del propio CV.
    """
    return dedent(prompt).strip()


def build_prompt_job_structuring(raw_job_description: str) -> str:
    """
    Construye el prompt para estructurar una descripción de puesto desordenada.
    Este prompt es opcional y puede utilizarse antes de optimizar el CV,
    para limpiar y organizar la descripción del puesto.
    """
    prompt = f"""
    Actúa como un analista de datos experto en Recursos Humanos.

    Tu tarea es tomar el siguiente texto de una descripción de puesto, que puede estar
    desordenado o contener información irrelevante, y estructurarlo de forma clara y concisa.

    Debes extraer la información esencial y organizarla en las siguientes secciones:

    - **Título del Puesto**
    - **Empresa**
    - **Área**
    - **Resumen del Rol**
    - **Perfil Buscado (Soft Skills)**
    - **Responsabilidades Clave**
    - **Requisitos Técnicos**

    Reglas de formato:
    1. Utiliza títulos en negrita para cada sección, por ejemplo: `**Título del Puesto:**`.
    2. Usa listas con guiones (`- `) para los puntos dentro de Perfil, Responsabilidades y Requisitos.
    3. Sé conciso y elimina información superflua como fechas de publicación, mensajes de marketing,
       frases genéricas o información que no describa el rol, el perfil o los requisitos.
    4. Si no encuentras información para una sección concreta, omite esa sección en el resultado final.

    Aquí está el texto en bruto para procesar:

    ---
    {raw_job_description}
    ---

    Devuelve únicamente el texto estructurado, sin comentarios, sin introducciones
    y sin explicaciones adicionales.
    """
    return dedent(prompt).strip()