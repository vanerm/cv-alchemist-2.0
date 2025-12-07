import streamlit as st
from src.extract_pdf import (
    extract_text_from_pdf,
    extract_text_from_multiple_pdfs,
)
from src.form_helpers import get_cv_form_data
from src.ai_service import generate_cv_output
from src.prompts import build_prompt_master, build_prompt_targeted


def process_uploaded_pdfs(files):
    """
    Procesa uno o varios archivos PDF subidos por el lector.

    - Si se recibe un único archivo, utiliza extract_text_from_pdf.
    - Si se recibe una lista de archivos, utiliza extract_text_from_multiple_pdfs.
    - Devuelve el texto extraído en formato string, ya normalizado.
    - Muestra mensajes de error en pantalla y devuelve None si algo falla.
    """
    try:
        # Caso: no se recibió nada.
        if not files:
            st.error("No se recibió ningún archivo PDF para procesar.")
            return None

        # Caso: un solo archivo UploadedFile.
        if not isinstance(files, list):
            files.seek(0)
            text = extract_text_from_pdf(files)
        else:
            # Lista de archivos (múltiples PDFs).
            # Si la lista tiene un solo elemento, también se puede reutilizar la función general.
            if len(files) == 1:
                files[0].seek(0)
                text = extract_text_from_pdf(files[0])
            else:
                text = extract_text_from_multiple_pdfs(files)

        # Normaliza el texto a un string limpio.
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
    """
    Función principal de la aplicación CV Alchemist 2.0.

    Permite:
    - Subir un CV base en PDF.
    - Subir uno o varios PDFs de nueva formación o plan de estudios.
    - Procesar ambos tipos de documentos.
    - Generar un CV Maestro actualizado mediante IA.
    """
    # Configuración básica de la página de Streamlit.
    st.set_page_config(page_title="CV Alchemist 2.0", layout="centered")

    # Inicialización de claves en session_state para almacenar texto de entrada y resultados.
    if "pdf_text_raw" not in st.session_state:
        st.session_state["pdf_text_raw"] = None

    if "pdf_text_clean" not in st.session_state:
        st.session_state["pdf_text_clean"] = None

    if "studies_text_clean" not in st.session_state:
        st.session_state["studies_text_clean"] = None

    if "cv_master" not in st.session_state:
        st.session_state["cv_master"] = None

    # Encabezado principal.
    st.title("CV Alchemist 2.0")
    st.subheader("Aplicación con IA para crear y optimizar CVs")

    # Selección del modo de uso.
    option = st.radio(
        "¿Qué desea hacer?",
        ["Subir un CV existente (PDF)", "Crear CV desde cero"],
        key="mode_selection",
    )

    # --------------------------------------------------------------------------
    # 🟦 OPCIÓN 1 — Subir CV existente en PDF
    # --------------------------------------------------------------------------
    if option == "Subir un CV existente (PDF)":
        st.markdown("### 1) Subir CV en formato PDF")

        uploaded_file = st.file_uploader(
            "Subir CV en formato PDF",
            type=["pdf"],
            help="El lector puede subir aquí su CV en archivo .pdf para analizarlo.",
        )

        # Botón para procesar el CV base.
        if uploaded_file and st.button("Procesar PDF"):
            cleaned_text = process_uploaded_pdfs(uploaded_file)

            if cleaned_text:
                # Guarda el texto del CV base en session_state.
                st.session_state["pdf_text_raw"] = cleaned_text
                st.session_state["pdf_text_clean"] = cleaned_text

                # Reinicia estados previos relacionados con formación y CV Maestro.
                st.session_state["studies_text_clean"] = None
                st.session_state["cv_master"] = None

                st.success("El PDF del CV se procesó correctamente.")

        # ----------------------------------------------------------------------
        # 🟦 Si ya existe un CV base procesado → permitir subir PDFs de estudios
        # ----------------------------------------------------------------------
        if st.session_state.get("pdf_text_clean"):
            st.markdown("### 2) Subir nueva formación / plan de estudios (PDFs)")

            study_files = st.file_uploader(
                label="Subir uno o varios PDFs de formación, cursos o planes de estudio",
                type=["pdf"],
                accept_multiple_files=True,
                help=(
                    "El lector puede subir aquí los PDFs de su nueva formación "
                    "(diplomaturas, cursos, certificaciones, programas académicos, etc.)."
                ),
                key="study_files_uploader",
            )

            # Botón para procesar los PDFs de formación.
            if study_files and st.button("Procesar PDFs"):
                studies_text_clean = process_uploaded_pdfs(study_files)

                if studies_text_clean:
                    st.session_state["studies_text_clean"] = studies_text_clean
                    st.session_state["cv_master"] = None

                    st.success("Los PDFs de formación se procesaron correctamente.")

            # ------------------------------------------------------------------
            # 🟦 Solo mostrar el botón de IA si ya se procesaron los estudios
            # ------------------------------------------------------------------
            if st.session_state.get("studies_text_clean"):
                st.markdown("### 3) Generar CV Maestro con IA")

                if st.button("Generar CV Maestro"):
                    # Construye el prompt combinado con CV base y nueva formación.
                    prompt = build_prompt_master(
                        cv_text=st.session_state["pdf_text_clean"],
                        new_studies=st.session_state["studies_text_clean"],
                    )

                    # Genera el CV Maestro mediante IA.
                    with st.spinner("Generando CV Maestro con IA..."):
                        cv_master = generate_cv_output(prompt)

                    st.session_state["cv_master"] = cv_master

            # ------------------------------------------------------------------
            # 🟦 Mostrar resultado final (si existe)
            # ------------------------------------------------------------------
            if st.session_state.get("cv_master"):
                st.markdown("### 4) Resultado: CV Maestro actualizado")
                st.text_area(
                    label="CV Maestro generado por IA",
                    value=st.session_state["cv_master"],
                    height=400,
                )

        else:
            # Aún no se procesó un CV base.
            st.info(
                "Una vez que el lector procese correctamente un PDF de CV, se habilitarán los "
                "pasos para subir la nueva formación en PDF y generar el CV Maestro."
            )

    # --------------------------------------------------------------------------
    # 🟦 OPCIÓN 2 — Crear CV desde cero
    # --------------------------------------------------------------------------
    else:
        st.info("Formulario para crear un CV desde cero (pendiente de completar).")
        # En una iteración futura se integrará get_cv_form_data() y la lógica
        # para construir CV Maestro y CV Target usando IA.


# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()