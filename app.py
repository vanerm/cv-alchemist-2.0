import streamlit as st
from src.extract_pdf import extract_text_from_pdf
from src.form_helpers import get_cv_form_data
from src.ai_service import generate_cv_output
from src.prompts import build_prompt_master, build_prompt_targeted

def main():
    st.set_page_config(page_title="CV Alchemist 2.0", layout="centered")

    st.title("CV Alchemist 2.0")
    st.subheader("Aplicación con IA para crear y optimizar tu CV")

    option = st.radio(
        "¿Qué querés hacer?",
        ["Subir un CV existente (PDF)", "Crear CV desde cero"],
        key="mode_selection"
    )

    if option == "Subir un CV existente (PDF)":
        uploaded_file = st.file_uploader("Subí tu CV en formato PDF", type=["pdf"])

        if uploaded_file:
            st.success("Archivo recibido correctamente.")
            # Lógica a implementar más adelante
            st.info("Extracción de texto pendiente de implementar.")

    else:
        st.info("Formulario para crear CV desde cero (pendiente de completar).")

if __name__ == "__main__":
    main()
