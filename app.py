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

    # Inicialización de claves en session_state para almacenar el texto del CV y resultados de IA.
    if "pdf_text_raw" not in st.session_state:
        st.session_state["pdf_text_raw"] = None

    if "pdf_text_clean" not in st.session_state:
        st.session_state["pdf_text_clean"] = None

    if "cv_master" not in st.session_state:
        st.session_state["cv_master"] = None

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
        st.markdown("### 1) Subir CV en formato PDF")

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

            except PDFExtractionError as e:
                # Muestra errores controlados de validación o extracción.
                st.error(f"Error al procesar el PDF: {e}")
            except Exception as e:
                # Muestra cualquier error inesperado para facilitar el debug.
                st.error(f"Error inesperado al procesar el archivo: {e}")

        # Si ya hay texto de CV disponible, se habilita la sección para generar el CV Maestro.
        if st.session_state.get("pdf_text_clean"):
            st.markdown("### 2) Agregar nueva formación / plan de estudios")

            new_studies = st.text_area(
                label="Describa la nueva formación, cursos o plan de estudios completados",
                value="",
                placeholder=(
                    "Ejemplo: Diplomatura en Data Science, CoderHouse. Contenidos: EDA, "
                    "modelos supervisados, dashboards en Power BI, etc."
                ),
                height=160,
                key="new_studies_input",
                help=(
                    "El lector puede pegar aquí el contenido de un plan de estudios, "
                    "programa académico o resumen de nuevos cursos realizados."
                ),
            )

            st.markdown("### 3) Generar CV Maestro con IA")

            if st.button("Generar CV Maestro"):
                if not new_studies.strip():
                    st.warning(
                        "Para generar el CV Maestro se recomienda describir la nueva formación "
                        "en el cuadro de texto anterior."
                    )
                else:
                    # Construye el prompt a partir del CV extraído y la nueva formación.
                    prompt = build_prompt_master(
                        cv_text=st.session_state["pdf_text_clean"],
                        new_studies=new_studies,
                    )

                    with st.spinner("Generando CV Maestro con IA..."):
                        cv_master = generate_cv_output(prompt)

                    st.session_state["cv_master"] = cv_master

            # Si ya existe un CV Maestro generado, se muestra al lector.
            if st.session_state.get("cv_master"):
                st.markdown("### 4) Resultado: CV Maestro actualizado")
                st.text_area(
                    label="CV Maestro generado por IA",
                    value=st.session_state["cv_master"],
                    height=400,
                )
        else:
            st.info(
                "Una vez que el lector procese correctamente un PDF, se habilitarán los "
                "pasos para agregar nueva formación y generar el CV Maestro."
            )

    # Opción 2: el lector crea un CV desde cero mediante un formulario guiado.
    else:
        st.info("Formulario para crear un CV desde cero (pendiente de completar).")
        # En una iteración posterior se integrará get_cv_form_data() y la lógica
        # para construir CV Maestro y CV Target usando IA.


if __name__ == "__main__":
    main()
