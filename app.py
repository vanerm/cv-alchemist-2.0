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
from src.ats_analyzer import analyze_ats_compatibility, get_score_color, get_score_emoji
from src.ui_styles import apply_custom_styles, render_header
from src.ui_components import create_sidebar
from src.form_validators import (
    validate_email,
    validate_phone,
    validate_name,
    validate_url,
    validate_text_length,
    sanitize_text,
    validate_company_name,
    validate_job_title,
)


def process_uploaded_pdfs(files):
    """
    Procesa uno o varios archivos PDF subidos por el lector con validación avanzada.
    """
    try:
        if not files:
            st.error("No se recibió ningún archivo PDF para procesar.")
            return None

        # Un solo archivo
        if not isinstance(files, list):
            text, validation = extract_text_from_pdf(files, validate=True)
            
            # Mostrar errores de validación
            if not validation.is_valid:
                st.error(f"❌ {validation.error_message}")
                return None
            
            # Mostrar advertencias si existen
            if validation.warning_message:
                st.warning(validation.warning_message)
            
            # Mostrar metadata
            if validation.metadata:
                meta = validation.metadata
                st.info(
                    f"📄 **PDF procesado:** {meta.get('num_pages', 0)} página(s) | "
                    f"{meta.get('text_length', 0)} caracteres extraídos | "
                    f"{meta.get('file_size_mb', 0)}MB"
                )
        else:
            # Lista de archivos
            if len(files) == 1:
                text, validation = extract_text_from_pdf(files[0], validate=True)
                
                if not validation.is_valid:
                    st.error(f"❌ {validation.error_message}")
                    return None
                
                if validation.warning_message:
                    st.warning(validation.warning_message)
                
                if validation.metadata:
                    meta = validation.metadata
                    st.info(
                        f"📄 **PDF procesado:** {meta.get('num_pages', 0)} página(s) | "
                        f"{meta.get('text_length', 0)} caracteres extraídos | "
                        f"{meta.get('file_size_mb', 0)}MB"
                    )
            else:
                text, validations = extract_text_from_multiple_pdfs(files, validate=True)
                
                # Verificar si hay errores
                errors = [v for v in validations if v and not v.is_valid]
                if errors:
                    for i, error in enumerate(errors):
                        st.error(f"❌ Archivo {i+1}: {error.error_message}")
                    return None
                
                # Mostrar advertencias
                warnings = [v for v in validations if v and v.warning_message]
                for warning in warnings:
                    st.warning(warning.warning_message)
                
                # Mostrar metadata consolidada
                total_pages = sum(v.metadata.get('num_pages', 0) for v in validations if v and v.metadata)
                total_chars = sum(v.metadata.get('text_length', 0) for v in validations if v and v.metadata)
                st.info(
                    f"📄 **{len(files)} PDFs procesados:** {total_pages} página(s) totales | "
                    f"{total_chars} caracteres extraídos"
                )

        text_clean = text.strip() if isinstance(text, str) else ""

        if not text_clean:
            st.error(
                "No se pudo extraer texto útil de los PDF(s). "
                "Es posible que sean documentos escaneados o sin contenido legible."
            )
            return None

        return text_clean

    except Exception as e:
        st.error(f"❌ Error inesperado al procesar los PDF(s): {e}")
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
    st.set_page_config(
        page_title="CV Alchemist 2.0",
        page_icon="🧪",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Aplicar estilos personalizados
    apply_custom_styles()
    
    # Crear sidebar
    create_sidebar()

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

    # Encabezado con estilo
    render_header(
        "CV Alchemist 2.0",
        "Aplicación con IA para crear y optimizar CVs profesionales"
    )

    # Importar templates antes de los flujos
    from src.cv_templates import get_template_names, get_template_by_display_name
    template_names = get_template_names()
    
    # Selección de modo con botón de reiniciar
    col_title, col_reset = st.columns([5, 1], gap="small")
    
    with col_title:
        st.markdown("### ¿Qué desea hacer?")
    
    with col_reset:
        st.markdown("<div style='margin-top: 0.3rem; text-align: right;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar", key="reset_button", help="Borrar todo y empezar de cero"):
            # Incrementar contador de reset para forzar recreación de file uploaders
            reset_count = st.session_state.get("reset_count", 0)
            # Limpiar todo el session_state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Restaurar contador incrementado
            st.session_state["reset_count"] = reset_count + 1
            st.rerun()
    
    # Inicializar contador de reset si no existe
    if "reset_count" not in st.session_state:
        st.session_state["reset_count"] = 0
    
    option = st.radio(
        "Seleccione una opción:",
        ["Subir un CV existente (PDF)", "Crear CV desde cero"],
        key="mode_selection",
        label_visibility="collapsed"
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
            key=f"cv_uploader_{st.session_state.get('reset_count', 0)}"
        )

        if uploaded_file and st.button("Procesar PDF"):
            with st.spinner("Procesando PDF del CV..."):
                cleaned_text = process_uploaded_pdfs(uploaded_file)

            if cleaned_text:
                st.session_state["pdf_text_raw"] = cleaned_text
                st.session_state["pdf_text_clean"] = cleaned_text
                st.session_state["studies_text_clean"] = None
                st.session_state["cv_master"] = None
                st.session_state["linkedin_profile"] = None
                st.session_state["cv_target"] = None
                st.session_state["job_description_raw"] = None
                st.session_state["show_success_pdf"] = True
                st.rerun()
        
        # Mostrar mensaje de éxito después del rerun
        if st.session_state.get("show_success_pdf"):
            st.success("El PDF del CV se procesó correctamente.")
            st.session_state["show_success_pdf"] = False

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
                key=f"study_files_uploader_{st.session_state.get('reset_count', 0)}",
            )

            # Procesar formación cargada
            if study_files and st.button("Procesar PDFs"):
                num_files = len(study_files) if isinstance(study_files, list) else 1
                with st.spinner(f"Procesando {num_files} PDF(s) de formación... Esto puede tomar unos momentos."):
                    studies_text_clean = process_uploaded_pdfs(study_files)

                if studies_text_clean:
                    st.session_state["studies_text_clean"] = studies_text_clean
                    st.session_state["cv_master"] = None
                    st.session_state["linkedin_profile"] = None
                    st.session_state["cv_target"] = None
                    st.session_state["show_success_studies"] = True
                    st.rerun()
            
            # Mostrar mensaje de éxito después del rerun
            if st.session_state.get("show_success_studies"):
                st.success("Los PDFs de formación se procesaron correctamente.")
                st.session_state["show_success_studies"] = False

            # Omitir formación y continuar (solo si no hay formación procesada)
            has_studies = st.session_state.get("studies_text_clean") not in [None, ""]
            
            if st.button(
                "➡️ Omitir formación y generar CV Maestro",
                disabled=has_studies,
                help="Ya se procesaron PDFs de formación" if has_studies else "Continuar sin agregar formación adicional"
            ):
                st.session_state["studies_text_clean"] = ""
                st.session_state["cv_master"] = None
                st.session_state["linkedin_profile"] = None
                st.session_state["cv_target"] = None
                st.session_state["show_info_skip"] = True
                st.rerun()
            
            # Mostrar mensaje después del rerun
            if st.session_state.get("show_info_skip"):
                st.info("Formación omitida. Ahora puedes generar el CV Maestro.")
                st.session_state["show_info_skip"] = False

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

                    provider = st.session_state.get("ai_provider", "auto")
                    model = st.session_state.get("ai_model")
                    
                    # Determinar nombre del modelo para mostrar
                    if provider == "auto":
                        model_name = "IA (OpenAI → Gemini)"
                    elif model:
                        model_name = model
                    else:
                        model_name = "IA"
                    
                    with st.spinner(f"Generando CV Maestro con {model_name}..."):
                        cv_master = generate_cv_output(prompt, model=model, provider=provider)

                    st.session_state["cv_master"] = cv_master
                    st.session_state["linkedin_profile"] = None
                    st.session_state["cv_target"] = None
                    st.rerun()

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
                
                # Selector de template
                selected_template = st.selectbox(
                    "🎨 Selecciona un template para el PDF",
                    template_names,
                    help="Elige el estilo visual para tu CV"
                )
                
                # Mostrar descripción del template
                tmpl = get_template_by_display_name(selected_template)
                st.caption(f"📝 {tmpl.description}")
                
                # Botón de descarga PDF
                pdf_bytes = generate_pdf(st.session_state["cv_master"], "CV Maestro", template=tmpl.name)
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

                    provider = st.session_state.get("ai_provider", "auto")
                    model = st.session_state.get("ai_model")
                    
                    # Determinar nombre del modelo para mostrar
                    if provider == "auto":
                        model_name = "IA (OpenAI → Gemini)"
                    elif model:
                        model_name = model
                    else:
                        model_name = "IA"
                    
                    with st.spinner(f"Generando perfil LinkedIn con {model_name}..."):
                        linkedin_profile = generate_cv_output(prompt_linkedin, model=model, provider=provider)

                    st.session_state["linkedin_profile"] = linkedin_profile
                    st.rerun()

                if st.session_state.get("linkedin_profile"):
                    st.text_area(
                        label="Perfil LinkedIn generado por IA",
                        value=st.session_state["linkedin_profile"],
                        height=350,
                        key="linkedin_output",
                    )
                    
                    # Selector de template para LinkedIn
                    selected_template_li = st.selectbox(
                        "🎨 Template para LinkedIn",
                        template_names,
                        key="template_linkedin",
                        help="Elige el estilo visual"
                    )
                    tmpl_li = get_template_by_display_name(selected_template_li)
                    st.caption(f"📝 {tmpl_li.description}")
                    
                    # Botón de descarga PDF
                    pdf_bytes_linkedin = generate_pdf(st.session_state["linkedin_profile"], "Perfil LinkedIn", template=tmpl_li.name)
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

                        provider = st.session_state.get("ai_provider", "auto")
                        model = st.session_state.get("ai_model")
                        
                        # Determinar nombre del modelo para mostrar
                        if provider == "auto":
                            model_name = "IA (OpenAI → Gemini)"
                        elif model:
                            model_name = model
                        else:
                            model_name = "IA"
                        
                        with st.spinner(f"Generando CV Target con {model_name}..."):
                            cv_target = generate_cv_output(prompt_target, model=model, provider=provider)

                        st.session_state["cv_target"] = cv_target
                        st.rerun()

                if st.session_state.get("cv_target"):
                    st.text_area(
                        label="CV Target generado por IA",
                        value=st.session_state["cv_target"],
                        height=400,
                        key="cv_target_output",
                    )
                    
                    # Selector de template para CV Target
                    selected_template_tg = st.selectbox(
                        "🎨 Template para CV Target",
                        template_names,
                        key="template_target",
                        help="Elige el estilo visual"
                    )
                    tmpl_tg = get_template_by_display_name(selected_template_tg)
                    st.caption(f"📝 {tmpl_tg.description}")
                    
                    # Botón de descarga PDF
                    pdf_bytes_target = generate_pdf(st.session_state["cv_target"], "CV Target", template=tmpl_tg.name)
                    st.download_button(
                        label="📥 Descargar CV Target (PDF)",
                        data=pdf_bytes_target,
                        file_name="cv_target.pdf",
                        mime="application/pdf",
                    )
                    
                    # ==============================================================
                    # 🟦 Análisis ATS del CV Target
                    # ==============================================================
                    st.markdown("---")
                    st.markdown("### 🔍 Análisis de Compatibilidad ATS")
                    st.caption("Evalúa qué tan bien tu CV pasará los sistemas de filtrado automático")
                    
                    if st.button("🔍 Analizar Compatibilidad ATS", key="analyze_ats_target"):
                        with st.spinner("Analizando compatibilidad ATS del CV Target..."):
                            ats_result = analyze_ats_compatibility(
                                cv_content=st.session_state["cv_target"],
                                job_description=st.session_state.get("job_description_raw", "")
                            )
                            st.session_state["ats_analysis"] = ats_result
                            st.rerun()
                    
                    # Mostrar resultados del análisis ATS
                    if st.session_state.get("ats_analysis"):
                        ats = st.session_state["ats_analysis"]
                        score = ats.get("score", 0)
                        
                        # Score principal con color
                        col_score, col_level = st.columns([1, 2])
                        with col_score:
                            st.metric(
                                "Score ATS",
                                f"{score}/100",
                                delta=None
                            )
                        with col_level:
                            emoji = get_score_emoji(score)
                            st.markdown(f"### {emoji} {ats.get('level', 'N/A')}")
                        
                        # Barra de progreso
                        st.progress(score / 100)
                        
                        # Fortalezas y Debilidades
                        col_str, col_weak = st.columns(2)
                        
                        with col_str:
                            st.markdown("**✅ Fortalezas**")
                            strengths = ats.get("strengths", [])
                            if strengths:
                                for strength in strengths:
                                    st.success(f"• {strength}")
                            else:
                                st.info("No se identificaron fortalezas específicas")
                        
                        with col_weak:
                            st.markdown("**⚠️ Debilidades**")
                            weaknesses = ats.get("weaknesses", [])
                            if weaknesses:
                                for weakness in weaknesses:
                                    st.warning(f"• {weakness}")
                            else:
                                st.info("No se identificaron debilidades críticas")
                        
                        # Palabras clave
                        st.markdown("**🔑 Análisis de Palabras Clave**")
                        col_found, col_missing = st.columns(2)
                        
                        with col_found:
                            st.markdown("*Encontradas:*")
                            kw_found = ats.get("keywords_found", [])
                            if kw_found:
                                st.write(", ".join(kw_found[:10]))  # Mostrar primeras 10
                            else:
                                st.caption("No especificadas")
                        
                        with col_missing:
                            st.markdown("*Faltantes:*")
                            kw_missing = ats.get("keywords_missing", [])
                            if kw_missing:
                                for kw in kw_missing[:5]:  # Mostrar primeras 5
                                    st.error(f"• {kw}")
                            else:
                                st.success("✓ Todas las palabras clave presentes")
                        
                        # Recomendaciones
                        st.markdown("**💡 Recomendaciones de Mejora**")
                        recommendations = ats.get("recommendations", [])
                        if recommendations:
                            for i, rec in enumerate(recommendations, 1):
                                st.info(f"{i}. {rec}")
                        else:
                            st.success("✓ No se requieren mejoras adicionales")
                        
                        # Detalles por criterio (expandible)
                        with st.expander("📊 Ver detalles por criterio"):
                            details = ats.get("details", {})
                            if details:
                                for criterion, detail in details.items():
                                    st.markdown(f"**{criterion}:** {detail}")
                            else:
                                st.caption("No hay detalles adicionales disponibles")

        else:
            st.info("Una vez procesado el PDF del CV, se habilitarán los pasos siguientes.")

    # ==========================================================================
    # 🟦 OPCIÓN 2 — Crear CV desde cero
    # ==========================================================================
    else:
        st.markdown("### 1) Completar formulario para crear CV base")

        # Definir listas de países y ciudades para reutilizar
        paises = [
            "Argentina", "Bolivia", "Chile", "Colombia", "Costa Rica",
            "Ecuador", "España", "Guatemala", "México", "Panamá",
            "Paraguay", "Perú", "Uruguay", "Venezuela", "Otro"
        ]
        
        ciudades_por_pais = {
            "Argentina": ["Buenos Aires", "Córdoba", "La Plata", "Mendoza", "Rosario", "Otra"],
            "México": ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "Otra"],
            "Colombia": ["Barranquilla", "Bogotá", "Cali", "Cartagena", "Medellín", "Otra"],
            "Chile": ["Antofagasta", "Concepción", "La Serena", "Santiago", "Valparaíso", "Otra"],
            "Perú": ["Arequipa", "Chiclayo", "Cusco", "Lima", "Trujillo", "Otra"],
            "España": ["Barcelona", "Bilbao", "Madrid", "Sevilla", "Valencia", "Otra"],
            "Uruguay": ["Maldonado", "Montevideo", "Paysandú", "Rivera", "Salto", "Otra"],
            "Otro": ["Especificar manualmente"]
        }

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
            
            pais = st.selectbox("País", paises, key="pais_select")
            
            if pais in ciudades_por_pais:
                ciudad = st.selectbox("Ciudad", ciudades_por_pais[pais], key="ciudad_select")
            else:
                ciudad = st.selectbox("Ciudad", ["Capital", "Otra"], key="ciudad_select_default")
            
            if ciudad in ["Otra", "Especificar manualmente"]:
                ciudad = st.text_input("Especificar ciudad", key="ciudad_manual")
            
            location = f"{ciudad}, {pais}" if ciudad and pais else ""

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
            # Ubicación del empleo con selectboxes
            col_pais, col_ciudad = st.columns(2)
            with col_pais:
                pais_job = st.selectbox(
                    f"País {i+1}",
                    paises,
                    key=f"pais_job_{i}",
                )
            with col_ciudad:
                if pais_job in ciudades_por_pais:
                    ciudad_job = st.selectbox(
                        f"Ciudad {i+1}",
                        ciudades_por_pais[pais_job],
                        key=f"ciudad_job_{i}",
                    )
                else:
                    ciudad_job = st.selectbox(
                        f"Ciudad {i+1}",
                        ["Capital", "Otra"],
                        key=f"ciudad_job_{i}",
                    )
            
            if ciudad_job in ["Otra", "Especificar manualmente"]:
                ciudad_job = st.text_input(f"Especificar ciudad {i+1}", key=f"ciudad_job_manual_{i}")
            
            location_job = f"{ciudad_job}, {pais_job}" if ciudad_job and pais_job else ""
            
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
                placeholder="Ej:\n• Análisis de métricas clave del área.\n• Automatización de reportes y procesos.\n• Mejora de procedimientos operativos.",
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
                placeholder="Ej: Sistema de reportes, Análisis de datos, etc.",
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
            placeholder="Ej: Herramientas técnicas relevantes, software especializado, habilidades blandas...",
            height=100,
        )

        submitted = st.button("Generar CV Maestro desde formulario")

        # Procesar envío del formulario
        if submitted:
            # Validaciones
            errors = []
            
            # Validar nombre
            is_valid, error_msg = validate_name(full_name)
            if not is_valid:
                errors.append(f"❌ Nombre: {error_msg}")
            
            # Validar email
            is_valid, error_msg = validate_email(email)
            if not is_valid:
                errors.append(f"❌ Email: {error_msg}")
            
            # Validar teléfono
            is_valid, error_msg = validate_phone(phone)
            if not is_valid:
                errors.append(f"❌ Teléfono: {error_msg}")
            
            # Validar titular
            is_valid, error_msg = validate_text_length(headline, 0, 200, "Titular profesional")
            if not is_valid:
                errors.append(f"❌ {error_msg}")
            
            # Validar resumen
            is_valid, error_msg = validate_text_length(summary, 0, 1000, "Resumen profesional")
            if not is_valid:
                errors.append(f"❌ {error_msg}")
            
            # Validar experiencias
            for i, exp in enumerate(experiences, 1):
                if exp.get("role"):
                    is_valid, error_msg = validate_job_title(exp["role"])
                    if not is_valid:
                        errors.append(f"❌ Puesto {i}: {error_msg}")
                
                if exp.get("company"):
                    is_valid, error_msg = validate_company_name(exp["company"])
                    if not is_valid:
                        errors.append(f"❌ Empresa {i}: {error_msg}")
                
                if exp.get("description"):
                    is_valid, error_msg = validate_text_length(exp["description"], 0, 2000, f"Descripción {i}")
                    if not is_valid:
                        errors.append(f"❌ {error_msg}")
            
            # Validar educación
            for i, edu in enumerate(educations, 1):
                if edu.get("degree"):
                    is_valid, error_msg = validate_text_length(edu["degree"], 0, 200, f"Título {i}")
                    if not is_valid:
                        errors.append(f"❌ {error_msg}")
                
                if edu.get("institution"):
                    is_valid, error_msg = validate_text_length(edu["institution"], 0, 200, f"Institución {i}")
                    if not is_valid:
                        errors.append(f"❌ {error_msg}")
            
            # Validar proyectos
            for i, proj in enumerate(projects, 1):
                if proj.get("name"):
                    is_valid, error_msg = validate_text_length(proj["name"], 0, 200, f"Nombre proyecto {i}")
                    if not is_valid:
                        errors.append(f"❌ {error_msg}")
                
                if proj.get("link"):
                    is_valid, error_msg = validate_url(proj["link"])
                    if not is_valid:
                        errors.append(f"❌ Proyecto {i} - {error_msg}")
                
                if proj.get("description"):
                    is_valid, error_msg = validate_text_length(proj["description"], 0, 1000, f"Descripción proyecto {i}")
                    if not is_valid:
                        errors.append(f"❌ {error_msg}")
            
            # Validar habilidades
            is_valid, error_msg = validate_text_length(skills, 0, 1000, "Habilidades")
            if not is_valid:
                errors.append(f"❌ {error_msg}")
            
            # Mostrar errores o procesar
            if errors:
                st.error("**Por favor corrige los siguientes errores:**")
                for error in errors:
                    st.error(error)
            else:
                # Sanitizar todos los campos de texto
                form_data = {
                    "full_name": sanitize_text(full_name),
                    "email": sanitize_text(email),
                    "phone": sanitize_text(phone),
                    "location": sanitize_text(location),
                    "headline": sanitize_text(headline),
                    "summary": sanitize_text(summary),
                    "experiences": [
                        {
                            "role": sanitize_text(exp.get("role", "")),
                            "company": sanitize_text(exp.get("company", "")),
                            "location": sanitize_text(exp.get("location", "")),
                            "from_date": exp.get("from_date"),
                            "to_date": exp.get("to_date"),
                            "is_current": exp.get("is_current", False),
                            "description": sanitize_text(exp.get("description", "")),
                        }
                        for exp in experiences
                    ],
                    "educations": [
                        {
                            "degree": sanitize_text(edu.get("degree", "")),
                            "institution": sanitize_text(edu.get("institution", "")),
                            "from_date": edu.get("from_date"),
                            "to_date": edu.get("to_date"),
                            "is_current": edu.get("is_current", False),
                        }
                        for edu in educations
                    ],
                    "projects": [
                        {
                            "name": sanitize_text(proj.get("name", "")),
                            "description": sanitize_text(proj.get("description", "")),
                            "link": sanitize_text(proj.get("link", "")),
                        }
                        for proj in projects
                    ],
                    "skills": sanitize_text(skills),
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

                provider = st.session_state.get("ai_provider", "auto")
                model = st.session_state.get("ai_model")
                
                # Determinar nombre del modelo para mostrar
                if provider == "auto":
                    model_name = "IA (OpenAI → Gemini)"
                elif model:
                    model_name = model
                else:
                    model_name = "IA"
                
                with st.spinner(f"Generando CV Maestro con {model_name}..."):
                    cv_master = generate_cv_output(prompt, model=model, provider=provider)

                st.session_state["cv_master"] = cv_master
                st.rerun()

        # Si ya hay CV Maestro generado desde el formulario, mostramos y permitimos LinkedIn / Target
        if st.session_state.get("cv_master"):
            st.markdown("### 2) Resultado: CV Maestro generado")

            st.text_area(
                label="CV Maestro generado por IA",
                value=st.session_state["cv_master"],
                height=400,
                key="cv_master_output_from_form",
            )
            
            # Selector de template
            selected_template_form = st.selectbox(
                "🎨 Template para el PDF",
                template_names,
                key="template_form",
                help="Elige el estilo visual"
            )
            tmpl_form = get_template_by_display_name(selected_template_form)
            st.caption(f"📝 {tmpl_form.description}")
            
            # Botón de descarga PDF
            pdf_bytes_form = generate_pdf(st.session_state["cv_master"], "CV Maestro", template=tmpl_form.name)
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

                provider = st.session_state.get("ai_provider", "auto")
                model = st.session_state.get("ai_model")
                
                # Determinar nombre del modelo para mostrar
                if provider == "auto":
                    model_name = "IA (OpenAI → Gemini)"
                elif model:
                    model_name = model
                else:
                    model_name = "IA"
                
                with st.spinner(f"Generando perfil LinkedIn con {model_name}..."):
                    linkedin_profile = generate_cv_output(prompt_linkedin, model=model, provider=provider)

                st.session_state["linkedin_profile"] = linkedin_profile
                st.rerun()

            if st.session_state.get("linkedin_profile"):
                st.text_area(
                    label="Perfil LinkedIn generado por IA",
                    value=st.session_state["linkedin_profile"],
                    height=350,
                    key="linkedin_output_from_form",
                )
                
                # Selector de template
                selected_template_li_form = st.selectbox(
                    "🎨 Template para LinkedIn",
                    template_names,
                    key="template_linkedin_form",
                    help="Elige el estilo visual"
                )
                tmpl_li_form = get_template_by_display_name(selected_template_li_form)
                st.caption(f"📝 {tmpl_li_form.description}")
                
                # Botón de descarga PDF
                pdf_bytes_linkedin_form = generate_pdf(st.session_state["linkedin_profile"], "Perfil LinkedIn", template=tmpl_li_form.name)
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

                    provider = st.session_state.get("ai_provider", "auto")
                    model = st.session_state.get("ai_model")
                    
                    # Determinar nombre del modelo para mostrar
                    if provider == "auto":
                        model_name = "IA (OpenAI → Gemini)"
                    elif model:
                        model_name = model
                    else:
                        model_name = "IA"
                    
                    with st.spinner(f"Generando CV Target con {model_name}..."):
                        cv_target = generate_cv_output(prompt_target, model=model, provider=provider)

                    st.session_state["cv_target"] = cv_target
                    st.rerun()

            if st.session_state.get("cv_target"):
                st.text_area(
                    label="CV Target generado por IA",
                    value=st.session_state["cv_target"],
                    height=400,
                    key="cv_target_output_from_form",
                )
                
                # Selector de template
                selected_template_tg_form = st.selectbox(
                    "🎨 Template para CV Target",
                    template_names,
                    key="template_target_form",
                    help="Elige el estilo visual"
                )
                tmpl_tg_form = get_template_by_display_name(selected_template_tg_form)
                st.caption(f"📝 {tmpl_tg_form.description}")
                
                # Botón de descarga PDF
                pdf_bytes_target_form = generate_pdf(st.session_state["cv_target"], "CV Target", template=tmpl_tg_form.name)
                st.download_button(
                    label="📥 Descargar CV Target (PDF)",
                    data=pdf_bytes_target_form,
                    file_name="cv_target.pdf",
                    mime="application/pdf",
                )
                
                # ==============================================================
                # 🟦 Análisis ATS del CV Target (desde formulario)
                # ==============================================================
                st.markdown("---")
                st.markdown("### 🔍 Análisis de Compatibilidad ATS")
                st.caption("Evalúa qué tan bien tu CV pasará los sistemas de filtrado automático")
                
                if st.button("🔍 Analizar Compatibilidad ATS", key="analyze_ats_form"):
                    with st.spinner("Analizando compatibilidad ATS del CV Target..."):
                        ats_result = analyze_ats_compatibility(
                            cv_content=st.session_state["cv_target"],
                            job_description=st.session_state.get("job_description_raw", "")
                        )
                        st.session_state["ats_analysis_form"] = ats_result
                        st.rerun()
                
                # Mostrar resultados del análisis ATS
                if st.session_state.get("ats_analysis_form"):
                    ats = st.session_state["ats_analysis_form"]
                    score = ats.get("score", 0)
                    
                    # Score principal con color
                    col_score, col_level = st.columns([1, 2])
                    with col_score:
                        st.metric(
                            "Score ATS",
                            f"{score}/100",
                            delta=None
                        )
                    with col_level:
                        emoji = get_score_emoji(score)
                        st.markdown(f"### {emoji} {ats.get('level', 'N/A')}")
                    
                    # Barra de progreso
                    st.progress(score / 100)
                    
                    # Fortalezas y Debilidades
                    col_str, col_weak = st.columns(2)
                    
                    with col_str:
                        st.markdown("**✅ Fortalezas**")
                        strengths = ats.get("strengths", [])
                        if strengths:
                            for strength in strengths:
                                st.success(f"• {strength}")
                        else:
                            st.info("No se identificaron fortalezas específicas")
                    
                    with col_weak:
                        st.markdown("**⚠️ Debilidades**")
                        weaknesses = ats.get("weaknesses", [])
                        if weaknesses:
                            for weakness in weaknesses:
                                st.warning(f"• {weakness}")
                        else:
                            st.info("No se identificaron debilidades críticas")
                    
                    # Palabras clave
                    st.markdown("**🔑 Análisis de Palabras Clave**")
                    col_found, col_missing = st.columns(2)
                    
                    with col_found:
                        st.markdown("*Encontradas:*")
                        kw_found = ats.get("keywords_found", [])
                        if kw_found:
                            st.write(", ".join(kw_found[:10]))  # Mostrar primeras 10
                        else:
                            st.caption("No especificadas")
                    
                    with col_missing:
                        st.markdown("*Faltantes:*")
                        kw_missing = ats.get("keywords_missing", [])
                        if kw_missing:
                            for kw in kw_missing[:5]:  # Mostrar primeras 5
                                st.error(f"• {kw}")
                        else:
                            st.success("✓ Todas las palabras clave presentes")
                    
                    # Recomendaciones
                    st.markdown("**💡 Recomendaciones de Mejora**")
                    recommendations = ats.get("recommendations", [])
                    if recommendations:
                        for i, rec in enumerate(recommendations, 1):
                            st.info(f"{i}. {rec}")
                    else:
                        st.success("✓ No se requieren mejoras adicionales")
                    
                    # Detalles por criterio (expandible)
                    with st.expander("📊 Ver detalles por criterio"):
                        details = ats.get("details", {})
                        if details:
                            for criterion, detail in details.items():
                                st.markdown(f"**{criterion}:** {detail}")
                        else:
                            st.caption("No hay detalles adicionales disponibles")


if __name__ == "__main__":
    main()