import streamlit as st
from src.extract_pdf import (
    validate_pdf,
    extract_text_from_pdf,
    clean_text,
    PDFExtractionError,
)
from src.form_helpers import get_cv_form_data
from src.ai_service import generate_cv_output
from src.prompts import build_prompt_master, build_prompt_targeted


def main():
    # Configuración básica de la página de Streamlit.
    st.set_page_config(page_title="CV Alchemist 2.0", layout="centered")

    # Inicialización de claves en session_state para almacenar el texto del CV.
    if "pdf_text_raw" not in st.session_state:
        st.session_state["pdf_text_raw"] = None

    if "pdf_text_clean" not in st.session_state:
        st.session_state["pdf_text_clean"] = None

    # Encabezado principal de la aplicación.
    st.title("CV Alchemist 2.0")
    st.subheader("Aplicación con IA para crear y optimizar CVs")

    # Selector de modo de uso: CV existente en PDF o CV desde cero.
    option = st.radio(
        "¿Qué desea hacer?",
        ["Subir un CV existente (PDF)", "Crear CV desde cero"],
        key="mode_selection",
    )

    # Opción 1: el lector sube un CV ya existente en formato PDF.
    if option == "Subir un CV existente (PDF)":
        uploaded_file = st.file_uploader(
            "Subir CV en formato PDF",
            type=["pdf"],
            help="El lector puede subir aquí su CV en archivo .pdf para analizarlo.",
        )

        # El procesamiento se dispara solo cuando el lector pulsa el botón.
        if uploaded_file and st.button("Procesar PDF"):
            try:
                # Valida el archivo recibido antes de procesarlo.
                validate_pdf(uploaded_file)

                # Posiciona el puntero al inicio del archivo antes de leerlo.
                uploaded_file.seek(0)

                # Extrae el texto del PDF mediante pdfplumber.
                raw_text = extract_text_from_pdf(uploaded_file)

                # Limpia y normaliza el texto extraído.
                cleaned_text = clean_text(raw_text)

                # Guarda el contenido en session_state para reutilizarlo luego
                # en la construcción de prompts y generación de CVs con IA.
                st.session_state["pdf_text_raw"] = raw_text
                st.session_state["pdf_text_clean"] = cleaned_text

                st.success("El PDF se procesó correctamente.")

                # Muestra una vista previa del texto procesado.
                with st.expander("Ver texto extraído (versión limpia)"):
                    st.text_area(
                        label="Texto procesado",
                        value=cleaned_text,
                        height=300,
                    )

            except PDFExtractionError as e:
                # Muestra errores controlados de validación o extracción.
                st.error(f"Error al procesar el PDF: {e}")
            except Exception as e:
                # Muestra cualquier error inesperado para facilitar el debug.
                st.error(f"Error inesperado al procesar el archivo: {e}")

    # Opción 2: el lector crea un CV desde cero mediante un formulario guiado.
    else:
        st.info("Formulario para crear un CV desde cero (pendiente de completar).")
        # En la siguiente iteración se integrará get_cv_form_data() y la lógica
        # para construir CV Maestro y CV Target usando IA.


if __name__ == "__main__":
    main()
