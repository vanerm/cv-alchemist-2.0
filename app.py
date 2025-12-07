import streamlit as st
from src.extract_pdf import (
    extract_text_from_pdf,
    extract_text_from_multiple_pdfs,
)
from src.form_helpers import get_cv_form_data
from src.ai_service import generate_cv_output
from src.prompts import (
    build_prompt_master,
    build_prompt_targeted,
    build_prompt_linkedin_profile,
)


# ------------------------------------------------------------
# Función unificada para procesar uno o varios PDFs
# ------------------------------------------------------------
def process_uploaded_pdfs(files):
    """
    Procesa uno o varios archivos PDF subidos por el lector.

    - Si se recibe un único archivo, utiliza extract_text_from_pdf.
    - Si se recibe una lista de archivos, utiliza extract_text_from_multiple_pdfs.
    - Devuelve el texto extraído en formato string, ya normalizado.
    - Muestra mensajes de error en pantalla y devuelve None si algo falla.
    """
    try:
        if not files:
            st.error("No se recibió ningún archivo PDF para procesar.")
            return None

        # Si es un único archivo UploadedFile (no lista)
        if not isinstance(files, list):
            files.seek(0)
            text = extract_text_from_pdf(files)
        else:
            if len(files) == 1:
                files[0].seek(0)
                text = extract_text_from_pdf(files[0])
            else:
                text = extract_text_from_multiple_pdfs(files)

        # Normalización
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


# ------------------------------------------------------------
# Aplicación principal
# ------------------------------------------------------------
def main():
    """Función principal de la aplicación CV Alchemist 2.0."""
    st.set_page_config(page_title="CV Alchemist 2.0", layout="centered")

    # Manejo automático de session_state
    for key in [
        "pdf_text_raw",
        "pdf_text_clean",
        "studies_text_clean",
        "cv_master",
        "linkedin_profile",
    ]:
        if key not in st.session_state:
            st.session_state[key] = None

    # Encabezado
    st.title("CV Alchemist 2.0")
    st.subheader("Aplicación con IA para crear y optimizar CVs")

    # Modo de uso
    option = st.radio(
        "¿Qué desea hacer?",
        ["Subir un CV existente (PDF)", "Crear CV desde cero"],
        key="mode_selection",
    )

    # ==========================================================
    # 🟦 OPCIÓN 1 — Subir CV existente
    # ==========================================================
    if option == "Subir un CV existente (PDF)":

        st.markdown("### 1) Subir CV en formato PDF")

        uploaded_file = st.file_uploader(
            "Subir CV en formato PDF",
            type=["pdf"],
            help="El lector puede subir aquí su CV en archivo .pdf para analizarlo.",
        )

        # Procesar CV base
        if uploaded_file and st.button("Procesar PDF"):
            cleaned_text = process_uploaded_pdfs(uploaded_file)

            if cleaned_text:
                st.session_state["pdf_text_raw"] = cleaned_text
                st.session_state["pdf_text_clean"] = cleaned_text

                # Reset de estados
                st.session_state["studies_text_clean"] = None
                st.session_state["cv_master"] = None
                st.session_state["linkedin_profile"] = None

                st.success("El PDF del CV se procesó correctamente.")

        # Si ya hay un CV base procesado → permitir estudios
        if st.session_state.get("pdf_text_clean"):

            st.markdown("### 2) Subir nueva formación / plan de estudios (PDFs)")

            study_files = st.file_uploader(
                label="Subir uno o varios PDFs de formación, cursos o planes de estudio",
                type=["pdf"],
                accept_multiple_files=True,
                help=(
                    "El lector puede subir aquí los PDFs de su nueva formación "
                    "(diplomaturas, cursos, certificaciones, etc.)."
                ),
                key="study_files_uploader",
            )

            if study_files and st.button("Procesar PDFs"):
                studies_text_clean = process_uploaded_pdfs(study_files)

                if studies_text_clean:
                    st.session_state["studies_text_clean"] = studies_text_clean
                    st.session_state["cv_master"] = None
                    st.session_state["linkedin_profile"] = None
                    st.success("Los PDFs de formación se procesaron correctamente.")

            # Si ya hay formación → permitir generación de CV Maestro
            if st.session_state.get("studies_text_clean"):

                st.markdown("### 3) Generar CV Maestro con IA")

                if st.button("Generar CV Maestro"):
                    prompt = build_prompt_master(
                        cv_text=st.session_state["pdf_text_clean"],
                        new_studies=st.session_state["studies_text_clean"],
                    )

                    with st.spinner("Generando CV Maestro con IA..."):
                        cv_master = generate_cv_output(prompt)

                    st.session_state["cv_master"] = cv_master
                    st.session_state["linkedin_profile"] = None

            # Mostrar CV Maestro
            if st.session_state.get("cv_master"):

                st.markdown("### 4) Resultado: CV Maestro actualizado")

                st.text_area(
                    label="CV Maestro generado por IA",
                    value=st.session_state["cv_master"],
                    height=400,
                    key="cv_master_output",
                )

                # ======================================================
                # 🟦 Sección nueva: Generar perfil de LinkedIn
                # ======================================================
                st.markdown("### 5) Generar versión para LinkedIn")

                if st.button("Generar Perfil LinkedIn"):
                    prompt_linkedin = build_prompt_linkedin_profile(
                        master_cv=st.session_state["cv_master"]
                    )

                    with st.spinner("Generando perfil LinkedIn con IA..."):
                        linkedin_profile = generate_cv_output(prompt_linkedin)

                    st.session_state["linkedin_profile"] = linkedin_profile

                # Mostrar resultado LinkedIn
                if st.session_state.get("linkedin_profile"):
                    st.text_area(
                        label="Perfil LinkedIn generado por IA",
                        value=st.session_state["linkedin_profile"],
                        height=350,
                        key="linkedin_output",
                    )

        else:
            st.info(
                "Una vez que el lector procese correctamente un PDF de CV, se habilitarán los pasos siguientes."
            )

    # ==========================================================
    # 🟦 OPCIÓN 2 — Crear CV desde cero
    # ==========================================================
    else:
        st.info("Formulario para crear un CV desde cero (pendiente de completar).")


# ------------------------------------------------------------
if __name__ == "__main__":
    main()