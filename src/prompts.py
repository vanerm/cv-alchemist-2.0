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

    Tu tarea es analizar dos documentos: el CV base de una persona y el contenido
    de un nuevo programa de estudios que ha completado.

    Tu misión es crear una nueva versión del CV, un "CV Maestro", que integre de forma
    profesional y coherente la nueva formación.

    Indicaciones clave:
    - Respeta estrictamente el estilo, orden y estructura del CV base. No reescribas
      secciones completas salvo para integrar la nueva formación y mejorar la claridad.
    - No añadas habilidades, tecnologías, herramientas, metodologías o aptitudes
      que no estén explícitamente presentes en el CV base o en los documentos de formación.
    - No inventes experiencia laboral, funciones, logros, títulos, cargos
      ni certificaciones.

    Reglas CRÍTICAS para evitar alucinaciones:
    - No inventes experiencia, funciones, logros ni títulos que no estén en el CV base
      o en los documentos de formación.
    - No añadas tecnologías, herramientas, lenguajes de programación ni metodologías
      que no aparezcan en el CV base o en la nueva formación.
    - No modifiques nombres de empresas, cargos, fechas ni duración de los empleos.
    - No atribuyas a ningún puesto actividades avanzadas (por ejemplo, uso de nuevas
      tecnologías especializadas, liderazgo de equipos, análisis cuantitativo complejo
      o diseño de modelos) si dichas actividades no están explícitamente descritas
      en la experiencia laboral del CV base.
    - Si el CV base o la nueva formación mencionan nuevas áreas técnicas, herramientas
      o metodologías solo en cursos, proyectos o certificaciones, puedes mencionarlas
      como parte de la formación o de los proyectos, pero NO como tareas formales
      realizadas en empleos pasados o actuales, a menos que se indique claramente.
    - El resumen profesional y las secciones deben dejar claro, cuando aplique,
      que se trata de una transición de carrera hacia un nuevo rol, y que parte
      de la experiencia práctica proviene de proyectos y formación, no de
      experiencia laboral directa.

    Estilo y estructura:
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
    - Evita expresiones excesivamente emocionales (por ejemplo, "me apasiona",
      "me encanta"). Prefiere un tono técnico, neutro y profesional.
    - Si el CV base incluye expresiones emocionales, puedes reescribirlas en un tono
      profesional y orientado a resultados, manteniendo el sentido pero reduciendo
      la carga emocional.
    - IMPORTANTE: NO agregues títulos o etiquetas como "Contactar", "Contacto",
      "Información de Contacto" antes del nombre y datos personales. El nombre y
      la información de contacto deben aparecer directamente al inicio sin ningún
      título previo.

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
    PROMPT TARGET — Versión ULTRA ESTRICTA y GENÉRICA.

    Reglas críticas para evitar alucinaciones:
    - No inventar experiencia laboral, funciones, logros, tecnologías, metodologías
      ni habilidades que NO estén explícitamente en el CV Maestro.
    - No inferir ni deducir tareas que “probablemente” se hayan realizado.
    - No convertir formación (cursos, diplomaturas, posgrados) ni proyectos académicos
      en experiencia laboral profesional.
    - No agregar herramientas, lenguajes, frameworks, técnicas, modelos, métricas
      ni certificaciones que no aparezcan en el CV Maestro.
    - No reescribir las responsabilidades laborales cambiando su significado.
      Solo se permite:
         * ordenar,
         * resumir,
         * mejorar la claridad,
      sin añadir actividades nuevas ni logros no mencionados.
    - No atribuir un nivel de seniority que no esté respaldado por el CV Maestro.

    Objetivo:
    Generar un CV orientado a un puesto específico (CV Target) que:
    - Mantenga la veracidad total de la información del CV Maestro.
    - Ajuste redacción, orden y énfasis para alinearse al puesto objetivo.
    - Respete la separación entre:
        * Experiencia laboral real
        * Formación / educación
        * Proyectos (académicos, personales o profesionales)

    El CV resultante debe incluir, cuando corresponda:
    - Resumen Profesional (honesto y factual, puede mencionar intención de transición)
    - Experiencia Profesional (sin inventar funciones ni logros)
    - Educación
    - Proyectos relevantes (solo si existen en el CV Maestro)
    - Habilidades / Aptitudes (solo las presentes en el CV Maestro)

    Optimización para ATS (con límites):
    - Solo se pueden usar palabras clave de la descripción del puesto que ya estén
      presentes en el CV Maestro (en experiencia, formación, proyectos o habilidades).
    - Si una palabra clave del puesto NO aparece en el CV Maestro, no debe agregarse.
    - Se permite reordenar y reagrupar secciones para mejorar legibilidad y
      compatibilidad ATS, pero sin cambiar hechos.

    Formato de salida:
    - Devuelve únicamente el texto final del CV Target, listo para copiar y pegar.
    - Sin comentarios adicionales, sin explicaciones y sin texto fuera del CV.
    """

    prompt = f"""
    Actúa como un experto en CVs y en sistemas ATS.

    Tu tarea es generar un **CV Target** orientado al puesto descrito,
    utilizando EXCLUSIVAMENTE la información contenida en el CV Maestro.

    --- INICIO DEL CV MAESTRO ---
    {master_cv}
    --- FIN DEL CV MAESTRO ---

    --- INICIO DE LA DESCRIPCIÓN DEL PUESTO ---
    {job_description}
    --- FIN DE LA DESCRIPCIÓN DEL PUESTO ---

    REGLAS OBLIGATORIAS (NO ROMPER NINGUNA):

    1) Veracidad total:
       - No inventes ninguna experiencia, responsabilidad, logro, herramienta,
         lenguaje, metodología, certificación ni habilidad que no figure en el CV Maestro.
       - No infieras tareas “probables” ni generalices funciones que no estén descritas.
       - No reformules responsabilidades laborales agregando acciones que no aparecen.

    2) Separación de categorías:
       - Distingue siempre entre:
           * Experiencia laboral
           * Formación (educación, cursos, diplomaturas, certificaciones)
           * Proyectos (académicos, personales o profesionales)
       - No conviertas formación ni proyectos en experiencia laboral.
       - No presentes proyectos académicos como si fueran puestos de trabajo.

    3) Uso de palabras clave del puesto:
       - Solo puedes usar términos, herramientas, técnicas o competencias que ya
         estén presentes en el CV Maestro (en experiencia, proyectos, formación o habilidades).
       - Si la descripción del puesto menciona algo que NO aparece en el CV Maestro,
         NO lo agregues al CV Target.
       - Puedes, como máximo, reorganizar y resaltar información ya existente para
         que el CV encaje mejor con el puesto, pero sin añadir contenido nuevo.

    4) Resumen Profesional:
       - Debe ser honesto, neutro y profesional.
       - Puede mencionar el interés o intención de transicionar al rol objetivo
         (por ejemplo, “orientado a…”, “buscando evolucionar hacia…”).
       - No puede atribuir experiencia práctica en herramientas o técnicas que solo
         aparecen como formación o en proyectos, salvo que el CV Maestro lo diga claramente.
       - No exageres el nivel de seniority ni la profundidad de experiencia.

    5) Estructura sugerida (puedes adaptarla según el CV Maestro):
       - Resumen Profesional
       - Experiencia Profesional
       - Educación / Formación
       - Proyectos Relevantes (si están en el CV Maestro)
       - Habilidades / Aptitudes

    SALIDA ESPERADA:
    - Genera únicamente el texto final del CV Target.
    - Sin explicaciones, sin comentarios y sin notas para la persona usuaria.
    - El resultado debe ser apto para pegarse directamente en una plantilla de CV.
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
    - Si el CV Maestro menciona nuevas áreas de especialización, herramientas
      o metodologías solo en formación o proyectos, se debe expresar como tal
      (formación/proyectos), no como tareas del rol actual si no está indicado.
    """
    prompt = f"""
    Actúa como especialista en Marca Personal y LinkedIn, con foco en perfiles
    profesionales de distintos campos (tecnología, negocio, datos, etc.).

    Tu tarea es leer el siguiente CV Maestro y, basándote EXCLUSIVAMENTE en su contenido,
    generar un PERFIL COMPLETO DE LINKEDIN que incluya:

    1) TITULAR (HEADLINE)
       - Máximo 120 caracteres.
       - Claro, profesional y fácil de entender.
       - No inventes tecnologías ni roles que no aparezcan en el CV Maestro.
       - Puedes mencionar formación en nuevas áreas (por ejemplo, un área técnica
         o de negocio distinta a la experiencia principal) si está en estudios
         o proyectos, pero no afirmes que el rol actual incluye esas tareas
         si el CV no lo dice.

    2) ACERCA DE (ABOUT)
       Debes devolver DOS versiones:
       - Versión breve: 3–4 líneas, ideal para alguien que quiere algo conciso.
       - Versión extendida: 1–2 párrafos, con más contexto y matices.
       
       Indicaciones:
       - Tono cálido, humano y profesional (apto para LinkedIn).
       - Menciona fortalezas reales basadas en el CV (por ejemplo:
         experiencia en determinados tipos de proyectos, responsabilidades
         en roles previos, formación relevante, etc.).
       - No afirmes que la persona aplica herramientas, metodologías o tecnologías
         específicas en su trabajo actual si el CV Maestro no lo indica explícitamente.
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
         coherente con eso (es válido como skill, pero no lo vincules al rol actual
         si no está indicado).

    4) DESTACADOS RECOMENDADOS (FEATURED)
       - Selecciona hasta 5 elementos del CV Maestro que podrían ir en “Destacados”:
         * Proyectos con enlaces (repositorios de código, dashboards, portfolios, etc.).
         * Publicaciones, blogs u otros trabajos relevantes.
       - Para cada uno, devuelve:
         - Un título corto
         - Una breve descripción (1 línea)
         - El enlace si está disponible en el CV Maestro
       - No inventes enlaces ni proyectos.

    Reglas CRÍTICAS para evitar alucinaciones:
    - No inventes tareas ni responsabilidades en empresas.
    - No digas que la persona usa herramientas o metodologías específicas
      en su rol actual si el CV Maestro no lo indica explícitamente.
    - Si el conocimiento en ciertos temas aparece en proyectos, cursos o diplomaturas,
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