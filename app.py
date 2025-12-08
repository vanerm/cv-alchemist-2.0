import streamlit as st
from src.extract_pdf import (
    extract_text_from_pdf,
    extract_text_from_multiple_pdfs,
)
from src.form_helpers import get_cv_form_data  # ahora no lo usamos, pero lo dejamos por compatibilidad
from src.ai_service import generate_cv_output
from src.prompts import (
    build_prompt_master,
    build_prompt_targeted,
    build_prompt_linkedin_profile,
)
from src.pdf_generator import generate_pdf


def process_uploaded_pdfs(files):
    """
    Procesa uno o varios archivos PDF subidos por el lector.
    """
    try:
        if not files:
            st.error("No se recibió ningún archivo PDF para procesar.")
            return None

        # Un solo archivo
        if not isinstance(files, list):
            files.seek(0)
            text = extract_text_from_pdf(files)
        else:
            # Lista de archivos
            if len(files) == 1:
                files[0].seek(0)
                text = extract_text_from_pdf(files[0])
            else:
                text = extract_text_from_multiple_pdfs(files)

        text_clean = text.strip() if isinstance(text, str) else ""

        if not text_clean:
            st.error(
                "No se pudo extraer texto útil de los PDF(s). "
                "Es posible que sean documentos escaneados o sin contenido legible."
            )
            return None

        return text_clean

    except Exception as e:
        st.error(f"Error inesperado al procesar los PDF(s): {e}")
        return None


# ----------------------------------------------------------------------
# Helper: construir texto de CV base a partir del formulario
# ----------------------------------------------------------------------
def _format_period_helper(from_date, to_date, is_current):
    """Helper para formatear periodos de fecha."""
    if not from_date and not to_date and not is_current:
        return ""
    
    from_str = from_date.strftime("%m/%Y") if from_date else ""
    
    if is_current:
        to_str = "Actualidad"
    elif to_date:
        to_str = to_date.strftime("%m/%Y")
    else:
        to_str = ""
    
    if from_str and to_str:
        return f"{from_str} – {to_str}"
    elif from_str:
        return from_str
    elif to_str:
        return to_str
    return ""


def build_cv_text_from_form(data: dict) -> str:
    """
    Recibe un diccionario con la info del formulario y construye
    un texto de CV base en formato similar al CV Maestro.
    """
    lines = []

    # Encabezado de contacto
    contact_line = " | ".join(
        [
            data.get("full_name", "").strip(),
            data.get("email", "").strip(),
            data.get("phone", "").strip(),
            data.get("location", "").strip(),
        ]
    ).strip(" |")

    if contact_line:
        lines.append(contact_line)
        lines.append("")

    # Titular
    headline = data.get("headline", "").strip()
    if headline:
        lines.append(headline)
        lines.append("")

    # Resumen profesional
    summary = data.get("summary", "").strip()
    if summary:
        lines.append("**Resumen Profesional**")
        lines.append(summary)
        lines.append("")

    # Experiencia profesional
    experiences = data.get("experiences", [])
    if experiences:
        lines.append("**Experiencia Profesional**")
        for exp in experiences:
            role = exp.get("role", "").strip()
            company = exp.get("company", "").strip()
            location = exp.get("location", "").strip()
            from_date = exp.get("from_date")
            to_date = exp.get("to_date")
            is_current = exp.get("is_current", False)
            desc = exp.get("description", "").strip()

            # Si está todo vacío, lo saltamos
            if not (role or company or desc):
                continue

            header_parts = []
            if company:
                header_parts.append(company)
            if role:
                header_parts.append(role)

            if header_parts:
                lines.append("**" + " — ".join(header_parts) + "**")

            meta_parts = []
            if location:
                meta_parts.append(location)
            
            dates_str = _format_period_helper(from_date, to_date, is_current)
            if dates_str:
                meta_parts.append(dates_str)
            
            if meta_parts:
                lines.append(" · ".join(meta_parts))

            if desc:
                lines.append(desc)

            lines.append("")

    # Educación
    educations = data.get("educations", [])
    if educations:
        lines.append("**Educación**")
        for edu in educations:
            degree = edu.get("degree", "").strip()
            institution = edu.get("institution", "").strip()
            from_date = edu.get("from_date")
            to_date = edu.get("to_date")
            is_current = edu.get("is_current", False)

            if not (degree or institution):
                continue

            title_parts = []
            if degree:
                title_parts.append(degree)
            if institution:
                title_parts.append(institution)

            lines.append(" · ".join(title_parts))

            dates_str = _format_period_helper(from_date, to_date, is_current)
            if dates_str:
                lines.append(dates_str)

        lines.append("")

    # Proyectos relevantes
    projects = data.get("projects", [])
    if projects:
        lines.append("**Proyectos Relevantes**")
        for proj in projects:
            name = proj.get("name", "").strip()
            desc = proj.get("description", "").strip()
            link = proj.get("link", "").strip()

            if not (name or desc or link):
                continue

            if name:
                lines.append(f"▶ **{name}**")
            if desc:
                lines.append(desc)
            if link:
                lines.append(link)

            lines.append("")

    # Habilidades
    skills = data.get("skills", "").strip()
    if skills:
        lines.append("**Habilidades**")
        lines.append(skills)

    # Unimos todo
    return "\n".join(lines).strip()


def main():
    """Función principal de la aplicación CV Alchemist 2.0."""
    st.set_page_config(page_title="CV Alchemist 2.0", layout="centered")

    # Manejo de session_state
    for key in [
        "pdf_text_raw",
        "pdf_text_clean",
        "studies_text_clean",
        "cv_master",
        "linkedin_profile",
        "cv_target",
        "job_description_raw",
    ]:
        if key not in st.session_state:
            st.session_state[key] = None

    # Encabezado
    st.title("CV Alchemist 2.0")
    st.subheader("Aplicación con IA para crear y optimizar CVs")

    # Selección de modo
    option = st.radio(
        "¿Qué desea hacer?",
        ["Subir un CV existente (PDF)", "Crear CV desde cero"],
        key="mode_selection",
    )

    # ==========================================================================
    # 🟦 OPCIÓN 1 — Subir CV existente
    # ==========================================================================
    if option == "Subir un CV existente (PDF)":

        st.markdown("### 1) Subir CV en formato PDF")

        uploaded_file = st.file_uploader(
            "Subir CV en formato PDF",
            type=["pdf"],
            help="El lector puede subir aquí su CV en archivo .pdf para analizarlo.",
        )

        if uploaded_file and st.button("Procesar PDF"):
            cleaned_text = process_uploaded_pdfs(uploaded_file)

            if cleaned_text:
                st.session_state["pdf_text_raw"] = cleaned_text
                st.session_state["pdf_text_clean"] = cleaned_text
                st.session_state["studies_text_clean"] = None
                st.session_state["cv_master"] = None
                st.session_state["linkedin_profile"] = None
                st.session_state["cv_target"] = None
                st.session_state["job_description_raw"] = None
                st.success("El PDF del CV se procesó correctamente.")

        # ----------------------------------------------------------------------
        # Subir PDFs de formación
        # ----------------------------------------------------------------------
        if st.session_state.get("pdf_text_clean"):

            st.markdown("### 2) Subir nueva formación / plan de estudios (PDFs)")

            study_files = st.file_uploader(
                label="Subir uno o varios PDFs de formación, cursos o planes de estudio",
                type=["pdf"],
                accept_multiple_files=True,
                help=(
                    "Puedes subir PDFs de formación O bien omitir este paso."
                ),
                key="study_files_uploader",
            )

            # Procesar formación cargada
            if study_files and st.button("Procesar PDFs"):
                studies_text_clean = process_uploaded_pdfs(study_files)

                if studies_text_clean:
                    st.session_state["studies_text_clean"] = studies_text_clean
                    st.session_state["cv_master"] = None
                    st.session_state["linkedin_profile"] = None
                    st.session_state["cv_target"] = None
                    st.success("Los PDFs de formación se procesaron correctamente.")

            # Omitir formación y continuar
            if st.button("➡️ Omitir formación y generar CV Maestro"):
                st.session_state["studies_text_clean"] = ""
                st.session_state["cv_master"] = None
                st.session_state["linkedin_profile"] = None
                st.session_state["cv_target"] = None
                st.info("Formación omitida. Ahora puedes generar el CV Maestro.")

            # ------------------------------------------------------------------
            # Generar CV Maestro si existe formación procesada O si fue omitida
            # ------------------------------------------------------------------
            if st.session_state.get("studies_text_clean") is not None:

                st.markdown("### 3) Generar CV Maestro con IA")

                if st.button("Generar CV Maestro"):
                    prompt = build_prompt_master(
                        cv_text=st.session_state["pdf_text_clean"],
                        new_studies=st.session_state["studies_text_clean"] or "",
                    )

                    with st.spinner("Generando CV Maestro con IA..."):
                        cv_master = generate_cv_output(prompt)

                    st.session_state["cv_master"] = cv_master
                    st.session_state["linkedin_profile"] = None
                    st.session_state["cv_target"] = None

            # ------------------------------------------------------------------
            # Mostrar CV Maestro generado
            # ------------------------------------------------------------------
            if st.session_state.get("cv_master"):

                st.markdown("### 4) Resultado: CV Maestro actualizado")

                st.text_area(
                    label="CV Maestro generado por IA",
                    value=st.session_state["cv_master"],
                    height=400,
                    key="cv_master_output",
                )
                
                # Botón de descarga PDF
                pdf_bytes = generate_pdf(st.session_state["cv_master"], "CV Maestro")
                st.download_button(
                    label="📥 Descargar CV Maestro (PDF)",
                    data=pdf_bytes,
                    file_name="cv_maestro.pdf",
                    mime="application/pdf",
                )

                # ==============================================================
                # 🟦 Sección 5: Generar Perfil LinkedIn
                # ==============================================================
                st.markdown("### 5) Generar versión para LinkedIn")

                if st.button("Generar Perfil LinkedIn"):
                    prompt_linkedin = build_prompt_linkedin_profile(
                        master_cv=st.session_state["cv_master"]
                    )

                    with st.spinner("Generando perfil LinkedIn con IA..."):
                        linkedin_profile = generate_cv_output(prompt_linkedin)

                    st.session_state["linkedin_profile"] = linkedin_profile

                if st.session_state.get("linkedin_profile"):
                    st.text_area(
                        label="Perfil LinkedIn generado por IA",
                        value=st.session_state["linkedin_profile"],
                        height=350,
                        key="linkedin_output",
                    )
                    
                    # Botón de descarga PDF
                    pdf_bytes_linkedin = generate_pdf(st.session_state["linkedin_profile"], "Perfil LinkedIn")
                    st.download_button(
                        label="📥 Descargar Perfil LinkedIn (PDF)",
                        data=pdf_bytes_linkedin,
                        file_name="perfil_linkedin.pdf",
                        mime="application/pdf",
                    )

                # ==============================================================
                # 🟦 Sección 6: Generar CV Target
                # ==============================================================
                st.markdown("### 6) Generar CV orientado a un puesto (CV Target)")

                st.session_state["job_description_raw"] = st.text_area(
                    label="Descripción del puesto objetivo",
                    value=st.session_state.get("job_description_raw") or "",
                    height=220,
                )

                if st.button("Generar CV Target"):
                    if not st.session_state.get("cv_master"):
                        st.warning(
                            "Primero necesita generar un CV Maestro antes de crear un CV Target."
                        )
                    elif not st.session_state["job_description_raw"].strip():
                        st.warning("Debe pegar la descripción del puesto.")
                    else:
                        prompt_target = build_prompt_targeted(
                            master_cv=st.session_state["cv_master"],
                            job_description=st.session_state["job_description_raw"],
                        )

                        with st.spinner("Generando CV Target con IA..."):
                            cv_target = generate_cv_output(prompt_target)

                        st.session_state["cv_target"] = cv_target

                if st.session_state.get("cv_target"):
                    st.text_area(
                        label="CV Target generado por IA",
                        value=st.session_state["cv_target"],
                        height=400,
                        key="cv_target_output",
                    )
                    
                    # Botón de descarga PDF
                    pdf_bytes_target = generate_pdf(st.session_state["cv_target"], "CV Target")
                    st.download_button(
                        label="📥 Descargar CV Target (PDF)",
                        data=pdf_bytes_target,
                        file_name="cv_target.pdf",
                        mime="application/pdf",
                    )

        else:
            st.info("Una vez procesado el PDF del CV, se habilitarán los pasos siguientes.")

    # ==========================================================================
    # 🟦 OPCIÓN 2 — Crear CV desde cero
    # ==========================================================================
    else:
        st.markdown("### 1) Completar formulario para crear CV base")

        # ----------------- Datos personales -----------------
        st.markdown("#### Datos personales")

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                "Nombre completo*",
                placeholder="Ej: Ana Pérez",
            )
            email = st.text_input(
                "Email*",
                placeholder="nombre@correo.com",
            )
            phone = st.text_input(
                "Teléfono",
                placeholder="+54 9 11 ...",
            )

        with col2:
            headline = st.text_input(
                "Titular profesional",
                placeholder="Ej: Analista de Datos Jr | Contador Público",
            )
            location = st.text_input(
                "Ubicación",
                placeholder="Ciudad, País",
            )

        summary = st.text_area(
            "Resumen profesional (opcional)",
            placeholder="Resume tu perfil en 3–4 líneas: experiencia principal, fortalezas y objetivo.",
            height=120,
        )

        # ----------------- Experiencia -----------------
        st.markdown("#### Experiencia profesional")
        n_exp = st.number_input(
            "Cantidad de empleos a incluir",
            min_value=0,
            max_value=10,
            value=1,
            step=1,
        )

        experiences = []
        for i in range(int(n_exp)):
            st.markdown(f"**Empleo {i+1}**")
            role = st.text_input(
                f"Puesto {i+1}",
                key=f"role_{i}",
                placeholder="Ej: Analista de Datos Jr",
            )
            company = st.text_input(
                f"Empresa {i+1}",
                key=f"company_{i}",
                placeholder="Ej: Mercado Libre",
            )
            location_job = st.text_input(
                f"Ubicación empleo {i+1}",
                key=f"location_job_{i}",
                placeholder="Ciudad, País",
            )
            
            col_d1, col_d2, col_d3 = st.columns([1, 1, 1])
            with col_d3:
                is_current = st.checkbox(
                    f"Actualidad {i+1}",
                    key=f"is_current_{i}",
                )
            with col_d1:
                from_date = st.date_input(
                    f"Desde {i+1}",
                    key=f"from_date_{i}",
                )
            with col_d2:
                to_date = st.date_input(
                    f"Hasta {i+1}",
                    key=f"to_date_{i}",
                    disabled=is_current,
                )
            desc = st.text_area(
                f"Responsabilidades / logros {i+1}",
                key=f"desc_{i}",
                placeholder="Ej:\n• Análisis de métricas clave.\n• Automatización de reportes en Excel / BI.\n• Mejora de procesos administrativos.",
                height=120,
            )

            experiences.append(
                {
                    "role": role,
                    "company": company,
                    "location": location_job,
                    "from_date": from_date,
                    "to_date": to_date,
                    "is_current": is_current,
                    "description": desc,
                }
            )

        # ----------------- Educación -----------------
        st.markdown("#### Educación")
        n_edu = st.number_input(
            "Cantidad de estudios a incluir",
            min_value=0,
            max_value=10,
            value=1,
            step=1,
        )

        educations = []
        for i in range(int(n_edu)):
            st.markdown(f"**Estudio {i+1}**")
            degree = st.text_input(
                f"Título / Programa {i+1}",
                key=f"degree_{i}",
                placeholder="Ej: Licenciatura en Economía | Diplomatura en Data Science",
            )
            institution = st.text_input(
                f"Institución {i+1}",
                key=f"institution_{i}",
                placeholder="Ej: UBA, Coderhouse, etc.",
            )
            col_e1, col_e2, col_e3 = st.columns([1, 1, 1])
            with col_e3:
                is_current_edu = st.checkbox(
                    f"En curso {i+1}",
                    key=f"is_current_edu_{i}",
                )
            with col_e1:
                from_date_edu = st.date_input(
                    f"Desde {i+1}",
                    key=f"from_date_edu_{i}",
                )
            with col_e2:
                to_date_edu = st.date_input(
                    f"Hasta {i+1}",
                    key=f"to_date_edu_{i}",
                    disabled=is_current_edu,
                )

            educations.append(
                {
                    "degree": degree,
                    "institution": institution,
                    "from_date": from_date_edu,
                    "to_date": to_date_edu,
                    "is_current": is_current_edu,
                }
            )

        # ----------------- Proyectos -----------------
        st.markdown("#### Proyectos (opcional)")
        n_proj = st.number_input(
            "Cantidad de proyectos a incluir",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
        )

        projects = []
        for i in range(int(n_proj)):
            st.markdown(f"**Proyecto {i+1}**")
            name = st.text_input(
                f"Nombre del proyecto {i+1}",
                key=f"proj_name_{i}",
                placeholder="Ej: Dashboard de Ventas en Power BI",
            )
            desc_proj = st.text_area(
                f"Descripción breve {i+1}",
                key=f"proj_desc_{i}",
                placeholder="Describe en 2–3 líneas el objetivo, herramientas y resultado.",
                height=100,
            )
            link = st.text_input(
                f"Enlace (GitHub, Tableau, Kaggle, etc.) {i+1}",
                key=f"proj_link_{i}",
                placeholder="https://...",
            )

            projects.append(
                {
                    "name": name,
                    "description": desc_proj,
                    "link": link,
                }
            )

        # ----------------- Habilidades -----------------
        st.markdown("#### Habilidades")
        skills = st.text_area(
            "Habilidades técnicas y blandas",
            placeholder="Ej: Python, SQL, Excel avanzado, Power BI, Comunicación, Trabajo en equipo...",
            height=100,
        )

        submitted = st.button("Generar CV Maestro desde formulario")

        # Procesar envío del formulario
        if submitted:
            if not full_name or not email:
                st.warning("Por favor completa al menos el nombre completo y el email.")
            else:
                form_data = {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "headline": headline,
                    "summary": summary,
                    "experiences": experiences,
                    "educations": educations,
                    "projects": projects,
                    "skills": skills,
                }

                cv_base_text = build_cv_text_from_form(form_data)

                # Reutilizamos el mismo pipeline que para PDF:
                st.session_state["pdf_text_raw"] = cv_base_text
                st.session_state["pdf_text_clean"] = cv_base_text
                st.session_state["studies_text_clean"] = ""  # sin plan de estudios extra
                st.session_state["linkedin_profile"] = None
                st.session_state["cv_target"] = None

                prompt = build_prompt_master(
                    cv_text=cv_base_text,
                    new_studies="",  # nada adicional
                )

                with st.spinner("Generando CV Maestro con IA a partir del formulario..."):
                    cv_master = generate_cv_output(prompt)

                st.session_state["cv_master"] = cv_master

        # Si ya hay CV Maestro generado desde el formulario, mostramos y permitimos LinkedIn / Target
        if st.session_state.get("cv_master"):
            st.markdown("### 2) Resultado: CV Maestro generado")

            st.text_area(
                label="CV Maestro generado por IA",
                value=st.session_state["cv_master"],
                height=400,
                key="cv_master_output_from_form",
            )
            
            # Botón de descarga PDF
            pdf_bytes_form = generate_pdf(st.session_state["cv_master"], "CV Maestro")
            st.download_button(
                label="📥 Descargar CV Maestro (PDF)",
                data=pdf_bytes_form,
                file_name="cv_maestro.pdf",
                mime="application/pdf",
            )

            # Perfil LinkedIn
            st.markdown("### 3) Generar versión para LinkedIn")

            if st.button("Generar Perfil LinkedIn (desde formulario)"):
                prompt_linkedin = build_prompt_linkedin_profile(
                    master_cv=st.session_state["cv_master"]
                )

                with st.spinner("Generando perfil LinkedIn con IA..."):
                    linkedin_profile = generate_cv_output(prompt_linkedin)

                st.session_state["linkedin_profile"] = linkedin_profile

            if st.session_state.get("linkedin_profile"):
                st.text_area(
                    label="Perfil LinkedIn generado por IA",
                    value=st.session_state["linkedin_profile"],
                    height=350,
                    key="linkedin_output_from_form",
                )
                
                # Botón de descarga PDF
                pdf_bytes_linkedin_form = generate_pdf(st.session_state["linkedin_profile"], "Perfil LinkedIn")
                st.download_button(
                    label="📥 Descargar Perfil LinkedIn (PDF)",
                    data=pdf_bytes_linkedin_form,
                    file_name="perfil_linkedin.pdf",
                    mime="application/pdf",
                )

            # CV Target
            st.markdown("### 4) Generar CV orientado a un puesto (CV Target)")

            st.session_state["job_description_raw"] = st.text_area(
                label="Descripción del puesto objetivo",
                value=st.session_state.get("job_description_raw") or "",
                height=220,
            )

            if st.button("Generar CV Target (desde formulario)"):
                if not st.session_state["job_description_raw"].strip():
                    st.warning("Debe pegar la descripción del puesto.")
                else:
                    prompt_target = build_prompt_targeted(
                        master_cv=st.session_state["cv_master"],
                        job_description=st.session_state["job_description_raw"],
                    )

                    with st.spinner("Generando CV Target con IA..."):
                        cv_target = generate_cv_output(prompt_target)

                    st.session_state["cv_target"] = cv_target

            if st.session_state.get("cv_target"):
                st.text_area(
                    label="CV Target generado por IA",
                    value=st.session_state["cv_target"],
                    height=400,
                    key="cv_target_output_from_form",
                )
                
                # Botón de descarga PDF
                pdf_bytes_target_form = generate_pdf(st.session_state["cv_target"], "CV Target")
                st.download_button(
                    label="📥 Descargar CV Target (PDF)",
                    data=pdf_bytes_target_form,
                    file_name="cv_target.pdf",
                    mime="application/pdf",
                )


if __name__ == "__main__":
    main()