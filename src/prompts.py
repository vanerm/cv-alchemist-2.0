# src/prompts.py
from textwrap import dedent


def build_prompt_master(cv_text: str, new_studies: str) -> str:
    """
    Construye el prompt para generar el CV Maestro actualizado.

    El lector debe pasar:
    - cv_text: texto del CV base (extraído del PDF o creado desde cero).
    - new_studies: texto descriptivo o extraído de la nueva formación / plan de estudios.

    El resultado estará pensado como CV formal:
    - Estilo ejecutivo, conciso y compatible con sistemas ATS.
    - Secciones claras (Resumen, Experiencia, Educación, Proyectos, Aptitudes, etc.).
    """
    prompt = f"""
    Actúa como un experto redactor de CVs y orientador profesional de alto nivel.

    Tu tarea es analizar dos documentos: el CV base de un candidato y el contenido
    de un nuevo programa de estudios que ha completado.

    Tu misión es crear una nueva versión del CV, un "CV Maestro", que integre de forma
    profesional y coherente la nueva formación.

    Indicaciones clave:
    - Respeta estrictamente el estilo, orden y estructura del CV base. No reescribas
      secciones completas salvo para integrar la nueva formación y mejorar la claridad.
    - No añadas habilidades, tecnologías o aptitudes que no estén explícitamente presentes
      en el CV base o en los documentos de formación.
    - No inventes experiencia laboral, títulos, cargos ni certificaciones.

    - No añadas ni asumas habilidades, herramientas, tecnologías, lenguajes
      de programación ni metodologías en empleos pasados o actuales que
      no estén presentes explícitamente en el CV base.
    - No atribuyas al rol actual en Mercado Libre (ni a ningún otro puesto)
      actividades relacionadas con:
          * análisis de datos
          * análisis exploratorio de datos (EDA)
          * SQL
          * Python
          * machine learning
          * visualización de datos
          * ciencia de datos en general
      a menos que aparezcan textualmente en el CV base.
    - No completes, infieras ni inventes tareas o funciones adicionales en
      roles laborales. Copia únicamente las responsabilidades que figuren
      en el CV base o que provengan de los documentos cargados.
    - No describas “optimización mediante datos”, “modelos”, “insights”
      o cualquier actividad analítica en empresas donde el CV base
      no lo mencione explícitamente.

    - Mantén un tono profesional, claro y directo.
    - Prioriza frases concisas y fáciles de escanear.
    - Organiza el resultado en secciones típicas de CV formal, por ejemplo:
        * Resumen Profesional
        * Experiencia Profesional
        * Educación
        * Proyectos Relevantes (si aplican)
        * Aptitudes Técnicas / Habilidades
        * Certificaciones (si las hubiera)
    - Usa viñetas para describir responsabilidades y logros cuando sea posible.
    - Evita párrafos muy largos; el CV debe ser fácil de leer en pocos segundos.
    - El resultado debe ser adecuado para exportarse a PDF y ser usado en postulaciones.

    - El resumen profesional debe ser breve, conciso y orientado a logros.
    - Evita expresiones emocionales (ej.: “me apasiona”, “me encanta”).
    - Mantén un tono técnico y profesional, adecuado para un CV formal.
    - Asegúrate de que la experiencia laboral destaque habilidades transferibles
      relevantes al análisis de datos únicamente cuando estas existan realmente
      en el CV base o en los documentos de formación.
    - Cuando el CV base incluya expresiones emocionales como “me apasiona”,
      “me encanta”, etc., reescríbelas en un tono profesional y orientado a logros.
      Esta reescritura está permitida aun cuando se respete la estructura del CV base.
    - Está permitido reescribir el Resumen Profesional para eliminar expresiones
      emocionales y reemplazarlas por un tono técnico, neutro y orientado a logros.

    A continuación se incluyen los documentos:

    --- INICIO DEL CV BASE ---
    {cv_text}
    --- FIN DEL CV BASE ---

    --- INICIO DEL PROGRAMA DE ESTUDIOS ---
    {new_studies}
    --- FIN DEL PROGRAMA DE ESTUDIOS ---

    Devuelve únicamente el texto completo del CV Maestro actualizado,
    listo para copiar y pegar en una plantilla de CV.
    No añadas comentarios, explicaciones ni encabezados externos.
    El formato debe ser texto plano con secciones claramente diferenciadas.
    """
    return dedent(prompt).strip()


def build_prompt_targeted(master_cv: str, job_description: str) -> str:
    """
    Construye el prompt para generar un CV optimizado para un puesto específico.

    El lector debe pasar:
    - master_cv: texto del CV Maestro actualizado.
    - job_description: descripción del puesto objetivo (idealmente ya estructurada).

    El resultado estará orientado a:
    - Alinear el CV Maestro con los requisitos del puesto.
    - Optimizar contenido y palabras clave para filtros ATS.
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

    Este prompt es opcional y permite:
    - Limpiar y organizar una descripción de puesto.
    - Extraer secciones clave como Perfil, Responsabilidades y Requisitos.
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

def build_prompt_linkedin_profile(master_cv: str) -> str:
    """
    Construye el prompt para generar un perfil completo de LinkedIn
    a partir del CV Maestro.

    El resultado debe incluir:
    - Titular (Headline)
    - Acerca de (versión breve y versión extendida)
    - Lista de habilidades (Skills) presentes en el CV
    - Destacados recomendados (Featured), basados en proyectos/enlaces reales

    IMPORTANTE:
    - No se debe inventar experiencia, tareas, tecnologías ni logros.
    - Si el CV Maestro menciona Data Science solo en formación o proyectos,
      se debe expresar como tal (formación/proyectos), no como tareas del rol actual.
    """
    prompt = f"""
    Actúa como especialista en Marca Personal y LinkedIn, con foco en perfiles
    de desarrollo de software y ciencia de datos.

    Tu tarea es leer el siguiente CV Maestro y, basándote EXCLUSIVAMENTE en su contenido,
    generar un PERFIL COMPLETO DE LINKEDIN que incluya:

    1) TITULAR (HEADLINE)
       - Máximo 120 caracteres.
       - Claro, profesional y fácil de entender.
       - No inventes tecnologías ni roles que no aparezcan en el CV Maestro.
       - Puedes mencionar formación en Data Science si está en estudios o proyectos,
         pero no afirmes que el rol actual incluye Data Science si el CV no lo dice.

    2) ACERCA DE (ABOUT)
       Debes devolver DOS versiones:
       - Versión breve: 3–4 líneas, ideal para alguien que quiere algo conciso.
       - Versión extendida: 1–2 párrafos, con más contexto y matices.
       
       Indicaciones:
       - Tono cálido, humano y profesional (apto para LinkedIn).
       - Menciona fortalezas reales basadas en el CV (por ejemplo:
         experiencia en desarrollo iOS, análisis funcional, proyectos de Data Science
         en formación o trabajos prácticos, etc., SOLO si aparecen en el CV).
       - No afirmes que la persona aplica ciencia de datos, machine learning, Python,
         SQL, etc. en su trabajo actual si eso no está explícitamente en el CV Maestro.
       - Puedes mencionar que está en formación o que realizó proyectos prácticos
         si eso figura en educación o proyectos.

    3) HABILIDADES (SKILLS)
       - Devuelve una lista de habilidades técnicas y blandas.
       - SOLO puedes incluir habilidades que aparezcan directa o indirectamente en:
         * Experiencia profesional
         * Educación
         * Proyectos
         * Certificaciones
       - No inventes herramientas, lenguajes ni frameworks.
       - Si una habilidad solo aparece en proyectos o formación, aclárala de manera
         coherente con eso (por ejemplo, es válido como skill, pero no lo vincules
         al rol actual si no está indicado).

    4) DESTACADOS RECOMENDADOS (FEATURED)
       - Selecciona hasta 5 elementos del CV Maestro que podrían ir en “Destacados” de LinkedIn:
         * Proyectos con enlaces (GitHub, Kaggle, Tableau, etc.).
         * Publicaciones o dashboards relevantes.
       - Para cada uno, devuelve:
         - Un título corto
         - Una breve descripción (1 línea)
         - El enlace si está disponible en el CV Maestro
       - No inventes enlaces ni proyectos.

    Reglas CRÍTICAS para evitar alucinaciones:
    - No inventes tareas ni responsabilidades en empresas (especialmente en el puesto actual).
    - No digas que la persona usa Data Science, Machine Learning, Python o SQL
      en su rol actual si el CV Maestro no lo indica explícitamente en la sección
      de experiencia laboral.
    - Si el conocimiento en Data Science aparece en proyectos, cursos o diplomaturas,
      delimítalo claramente como formación o práctica en proyectos, no como experiencia
      laboral profesional.
    - No agregues certificaciones, cursos o herramientas que no existan en el CV Maestro.

    FORMATO DE RESPUESTA (muy importante):
    Devuelve el resultado exactamente con esta estructura de secciones:

    **Titular (Headline)**
    [una sola línea con el titular]

    **Acerca de — versión breve**
    [3–4 líneas de texto]

    **Acerca de — versión extendida**
    [1–2 párrafos de texto]

    **Habilidades (Skills)**
    - Skill 1
    - Skill 2
    - Skill 3
    ...

    **Destacados recomendados (Featured)**
    - Título 1 — breve descripción. Enlace: [URL si existe en el CV]
    - Título 2 — breve descripción. Enlace: [URL si existe en el CV]
    - ...

    Aquí tienes el CV Maestro completo para usar como única fuente de verdad:

    --- INICIO DEL CV MAESTRO ---
    {master_cv}
    --- FIN DEL CV MAESTRO ---
    """
    return dedent(prompt).strip()