import streamlit as st
from src.extract_pdf import (
    extract_text_from_pdf,
    extract_text_from_multiple_pdfs,
)
# from src.form_helpers import get_cv_form_data  # ya no lo usamos en esta versión
from src.ai_service import generate_cv_output
from src.prompts import (
    build_prompt_master,
    build_prompt_targeted,
    build_prompt_linkedin_profile,
)


def process_uploaded_pdfs(files):
    """
    Procesa uno o varios archivos PDF subidos por el lector.
    """
    try:
        if not files:
            st.error("No se recibió ningún archivo PDF para procesar.")
            return None

        if not isinstance(files, list):
            files.seek(0)
            text = extract_text_from_pdf(files)
        else:
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

        else:
            st.info("Una vez procesado el PDF del CV, se habilitarán los pasos siguientes.")

    # ==========================================================================
    # 🟦 OPCIÓN 2 — Crear CV desde cero
    # ==========================================================================
    else:
        st.markdown("### 1) Completar formulario para crear CV base")

        with st.form("cv_from_scratch_form"):
            name = st.text_input("Nombre completo")
            email = st.text_input("Email de contacto")
            phone = st.text_input("Teléfono (opcional)")
            location = st.text_input("Ubicación (ciudad, país)")
            headline = st.text_input("Titular profesional (opcional)")
            profile = st.text_area("Resumen profesional / Perfil")
            experience = st.text_area(
                "Experiencia profesional (puedes listar puestos, fechas y funciones)"
            )
            education = st.text_area(
                "Educación / Formación (títulos, instituciones, fechas)"
            )
            projects = st.text_area(
                "Proyectos relevantes (opcional: proyectos personales, académicos, etc.)"
            )
            skills = st.text_area(
                "Habilidades (separadas por coma: ej. Excel, SQL, Comunicación)"
            )

            submitted = st.form_submit_button("Guardar CV base")

        if submitted:
            # Construimos un CV base en texto plano
            lines = []

            # Encabezado de contacto
            contact_parts = [p for p in [name, email, phone, location] if p]
            if contact_parts:
                lines.append(" | ".join(contact_parts))
                lines.append("")

            if headline:
                lines.append(headline)
                lines.append("")

            if profile:
                lines.append("**Resumen Profesional**")
                lines.append(profile.strip())
                lines.append("")

            if experience:
                lines.append("**Experiencia Profesional**")
                lines.append(experience.strip())
                lines.append("")

            if education:
                lines.append("**Educación**")
                lines.append(education.strip())
                lines.append("")

            if projects:
                lines.append("**Proyectos Relevantes**")
                lines.append(projects.strip())
                lines.append("")

            if skills:
                lines.append("**Habilidades**")
                # dejamos tal cual, el usuario puede poner comas o viñetas
                lines.append(skills.strip())
                lines.append("")

            base_cv_text = "\n".join(lines).strip()

            if not base_cv_text:
                st.warning("Por favor completa al menos algún campo para generar el CV base.")
            else:
                st.session_state["pdf_text_raw"] = base_cv_text
                st.session_state["pdf_text_clean"] = base_cv_text
                st.session_state["studies_text_clean"] = ""
                st.session_state["cv_master"] = None
                st.session_state["linkedin_profile"] = None
                st.session_state["cv_target"] = None
                st.session_state["job_description_raw"] = None
                st.success("Datos del formulario cargados. Ahora puedes generar el CV Maestro con IA.")

        # Si ya tenemos un CV base desde el formulario, habilitamos el flujo IA
        if st.session_state.get("pdf_text_clean"):

            st.markdown("### 2) Generar CV Maestro con IA")

            if st.button("Generar CV Maestro desde formulario"):
                prompt = build_prompt_master(
                    cv_text=st.session_state["pdf_text_clean"],
                    new_studies="",  # aquí no hay PDFs de formación adicionales
                )

                with st.spinner("Generando CV Maestro con IA..."):
                    cv_master = generate_cv_output(prompt)

                st.session_state["cv_master"] = cv_master
                st.session_state["linkedin_profile"] = None
                st.session_state["cv_target"] = None

            # Mostrar CV Maestro
            if st.session_state.get("cv_master"):

                st.markdown("### 3) Resultado: CV Maestro generado")

                st.text_area(
                    label="CV Maestro generado por IA",
                    value=st.session_state["cv_master"],
                    height=400,
                    key="cv_master_output_from_form",
                )

                # --------------------------------------------------------------
                # Perfil LinkedIn
                # --------------------------------------------------------------
                st.markdown("### 4) Generar versión para LinkedIn")

                if st.button("Generar Perfil LinkedIn desde CV Maestro"):
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

                # --------------------------------------------------------------
                # CV Target
                # --------------------------------------------------------------
                st.markdown("### 5) Generar CV orientado a un puesto (CV Target)")

                st.session_state["job_description_raw"] = st.text_area(
                    label="Descripción del puesto objetivo",
                    value=st.session_state.get("job_description_raw") or "",
                    height=220,
                    key="job_description_input_from_form",
                )

                if st.button("Generar CV Target desde formulario"):
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
                        key="cv_target_output_from_form",
                    )


if __name__ == "__main__":
    main()
