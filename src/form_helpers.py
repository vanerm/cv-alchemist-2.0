# src/form_helpers.py

from __future__ import annotations

from datetime import date
from textwrap import dedent

import streamlit as st


def _format_period(from_date: date | None,
                   to_date: date | None,
                   is_current: bool) -> str:
    """
    Devuelve un período en formato 'MM/YYYY – MM/YYYY' o 'MM/YYYY – Actualidad'.
    Si no hay fechas, devuelve cadena vacía.
    """
    if not from_date and not to_date and not is_current:
        return ""

    if from_date:
        from_str = from_date.strftime("%m/%Y")
    else:
        from_str = ""

    if is_current:
        to_str = "Actualidad"
    elif to_date:
        to_str = to_date.strftime("%m/%Y")
    else:
        to_str = ""

    if from_str and to_str:
        return f"{from_str} – {to_str}"
    elif from_str and not to_str:
        return from_str
    elif not from_str and to_str:
        return to_str
    else:
        return ""


def get_cv_form_data() -> str | None:
    """
    Dibuja el formulario para crear un CV base desde cero y devuelve
    el texto del CV en formato plano cuando el usuario pulsa el botón
    "Generar CV Maestro desde formulario".

    Si faltan datos mínimos o no se pulsa el botón, devuelve None.
    """
    st.markdown("### 1) Completar formulario para crear CV base")

    # ------------------------------------------------------------------
    # 1) Datos personales
    # ------------------------------------------------------------------
    nombre = st.text_input(
        "Nombre completo*",
        key="form_nombre",
        placeholder="Ej: Vanesa Mizrahi",
    )

    email = st.text_input(
        "Email*",
        key="form_email",
        placeholder="Ej: nombre@correo.com",
    )

    telefono = st.text_input(
        "Teléfono",
        key="form_telefono",
        placeholder="Ej: +54 11 1234 5678",
    )

    ubicacion = st.text_input(
        "Ubicación",
        key="form_ubicacion",
        placeholder="Ej: Ciudad Autónoma de Buenos Aires, Argentina",
    )

    titular = st.text_input(
        "Titular profesional (headline)",
        key="form_headline",
        placeholder="Ej: Analista de Datos Jr | Desarrolladora iOS | Estudiante de Data Science",
    )

    resumen = st.text_area(
        "Resumen profesional (opcional)",
        key="form_resumen",
        placeholder="Resume tu perfil en 3–4 líneas: experiencia principal, fortalezas y objetivo.",
        height=120,
    )

    st.markdown("---")

    # ------------------------------------------------------------------
    # 2) Experiencia profesional
    # ------------------------------------------------------------------
    st.markdown("#### Experiencia profesional")

    jobs_count = st.number_input(
        "Cantidad de empleos a incluir",
        min_value=0,
        max_value=10,
        step=1,
        key="jobs_count",
    )

    jobs = []
    for i in range(1, int(jobs_count) + 1):
        st.markdown(f"**Empleo {i}**")

        puesto = st.text_input(
            f"Puesto {i}",
            key=f"form_puesto_{i}",
            placeholder="Ej: Analista de Datos Jr",
        )
        empresa = st.text_input(
            f"Empresa {i}",
            key=f"form_empresa_{i}",
            placeholder="Ej: Mercado Libre",
        )
        ubic_emp = st.text_input(
            f"Ubicación empleo {i}",
            key=f"form_ubic_empleo_{i}",
            placeholder="Ej: Ciudad, País",
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            from_date = st.date_input(
                f"Desde {i}",
                key=f"form_from_{i}",
                help="Fecha de inicio del empleo.",
            )
        with col2:
            to_date = st.date_input(
                f"Hasta {i}",
                key=f"form_to_{i}",
                help="Fecha de fin (si aplica).",
            )
        with col3:
            is_current = st.checkbox(
                f"Actualmente aquí {i}",
                key=f"form_current_{i}",
                help="Marca si este es tu empleo actual.",
            )

        resp = st.text_area(
            f"Responsabilidades / logros {i}",
            key=f"form_resp_{i}",
            placeholder=(
                "Ej:\n"
                "• Análisis de métricas clave.\n"
                "• Automatización de reportes en Excel / BI.\n"
                "• Mejora de procesos administrativos."
            ),
            height=120,
        )

        jobs.append(
            {
                "puesto": puesto.strip(),
                "empresa": empresa.strip(),
                "ubicacion": ubic_emp.strip(),
                "from_date": from_date,
                "to_date": to_date,
                "is_current": is_current,
                "responsabilidades": resp.strip(),
            }
        )

        st.markdown("---")

    # ------------------------------------------------------------------
    # 3) Educación
    # ------------------------------------------------------------------
    st.markdown("#### Educación")

    edu_count = st.number_input(
        "Cantidad de estudios a incluir",
        min_value=0,
        max_value=10,
        step=1,
        key="edu_count",
    )

    educations = []
    for i in range(1, int(edu_count) + 1):
        st.markdown(f"**Estudio {i}**")
        titulo = st.text_input(
            f"Título / Programa {i}",
            key=f"form_edu_titulo_{i}",
            placeholder="Ej: Diplomatura en Data Science",
        )
        institucion = st.text_input(
            f"Institución {i}",
            key=f"form_edu_inst_{i}",
            placeholder="Ej: UBA, Coderhouse, etc.",
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            edu_from = st.date_input(
                f"Desde estudio {i}",
                key=f"form_edu_from_{i}",
            )
        with col2:
            edu_to = st.date_input(
                f"Hasta estudio {i}",
                key=f"form_edu_to_{i}",
            )
        with col3:
            edu_current = st.checkbox(
                f"En curso {i}",
                key=f"form_edu_current_{i}",
            )

        educations.append(
            {
                "titulo": titulo.strip(),
                "institucion": institucion.strip(),
                "from_date": edu_from,
                "to_date": edu_to,
                "is_current": edu_current,
            }
        )

        st.markdown("---")

    # ------------------------------------------------------------------
    # 4) Proyectos (opcional)
    # ------------------------------------------------------------------
    st.markdown("#### Proyectos (opcional)")

    proj_count = st.number_input(
        "Cantidad de proyectos a incluir",
        min_value=0,
        max_value=10,
        step=1,
        key="proj_count",
    )

    projects = []
    for i in range(1, int(proj_count) + 1):
        st.markdown(f"**Proyecto {i}**")
        nombre_proj = st.text_input(
            f"Nombre del proyecto {i}",
            key=f"form_proj_nombre_{i}",
            placeholder="Ej: Olist Marketplace – Data Science",
        )
        desc_proj = st.text_area(
            f"Descripción breve {i}",
            key=f"form_proj_desc_{i}",
            placeholder="Describe en 2–3 líneas qué hiciste, herramientas usadas y objetivo.",
            height=100,
        )
        link_proj = st.text_input(
            f"Enlace (GitHub, Kaggle, Tableau, etc.) {i}",
            key=f"form_proj_link_{i}",
            placeholder="Ej: https://github.com/usuario/proyecto",
        )

        projects.append(
            {
                "nombre": nombre_proj.strip(),
                "descripcion": desc_proj.strip(),
                "link": link_proj.strip(),
            }
        )

        st.markdown("---")

    # ------------------------------------------------------------------
    # 5) Habilidades
    # ------------------------------------------------------------------
    st.markdown("#### Habilidades")

    habilidades = st.text_area(
        "Habilidades técnicas y blandas",
        key="form_habilidades",
        placeholder=(
            "Ej: Python, SQL, Excel avanzado, Power BI, Comunicación, Trabajo en equipo..."
        ),
        height=100,
    )

    # ------------------------------------------------------------------
    # BOTÓN: Generar CV
    # ------------------------------------------------------------------
    if not st.button("Generar CV Maestro desde formulario"):
        return None

    # Validaciones mínimas
    if not nombre.strip() or not email.strip():
        st.warning("Por favor completá al menos el nombre completo y el email.")
        return None

    # ------------------------------------------------------------------
    # Construcción del texto del CV
    # ------------------------------------------------------------------
    lines = []

    # Contacto
    contacto_line = " | ".join(
        [
            nombre.strip(),
            email.strip(),
            telefono.strip() if telefono.strip() else "",
            ubicacion.strip() if ubicacion.strip() else "",
        ]
    ).strip(" |")
    lines.append(contacto_line)
    lines.append("")  # línea en blanco

    # Titular
    if titular.strip():
        lines.append(titular.strip())
        lines.append("")

    # Resumen
    if resumen.strip():
        lines.append("**Resumen Profesional**")
        lines.append(resumen.strip())
        lines.append("")

    # Experiencia
    if any(j["puesto"] or j["empresa"] for j in jobs):
        lines.append("**Experiencia Profesional**")
        for j in jobs:
            if not j["puesto"] and not j["empresa"]:
                continue

            header = " / ".join(
                [x for x in [j["puesto"], j["empresa"], j["ubicacion"]] if x]
            )
            if header:
                lines.append(header)

            period_str = _format_period(
                j["from_date"], j["to_date"], j["is_current"]
            )
            if period_str:
                lines.append(period_str)

            if j["responsabilidades"]:
                lines.append(j["responsabilidades"])
            lines.append("")
        lines.append("")

    # Educación
    if any(e["titulo"] or e["institucion"] for e in educations):
        lines.append("**Educación**")
        for e in educations:
            if not e["titulo"] and not e["institucion"]:
                continue

            header = " | ".join(
                [x for x in [e["titulo"], e["institucion"]] if x]
            )
            if header:
                lines.append(header)

            period_str = _format_period(
                e["from_date"], e["to_date"], e["is_current"]
            )
            if period_str:
                lines.append(period_str)

            lines.append("")
        lines.append("")

    # Proyectos
    if any(p["nombre"] for p in projects):
        lines.append("**Proyectos Relevantes**")
        for p in projects:
            if not p["nombre"]:
                continue

            line = f"▶ {p['nombre']}"
            lines.append(line)
            if p["descripcion"]:
                lines.append(p["descripcion"])
            if p["link"]:
                lines.append(f"Enlace: {p['link']}")
            lines.append("")
        lines.append("")

    # Habilidades
    if habilidades.strip():
        lines.append("**Habilidades**")
        lines.append(habilidades.strip())
        lines.append("")

    cv_text = "\n".join(lines).strip()
    return dedent(cv_text)
