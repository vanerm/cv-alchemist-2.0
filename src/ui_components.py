# src/ui_components.py

"""
Componentes reutilizables de UI para la aplicación.
Incluye sidebar, progress tracker, cards, etc.
"""

import streamlit as st


def create_sidebar():
    """Crea sidebar con navegación y estado del progreso."""
    with st.sidebar:
        # Logo/Header
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="margin: 0; color: #667eea;">🧪 CV Alchemist</h2>
                <p style="margin: 0.5rem 0 0 0; color: #2C3E50; font-size: 0.9rem; font-weight: 600;">
                    Versión 2.0
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Selector de modelo de IA
        st.markdown("### 🤖 Modelo de IA")
        
        # Modelos disponibles de OpenAI
        openai_models = [
            "gpt-4o-mini (recomendado)",
            "gpt-4o",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo"
        ]
        
        gemini_models = [
            "gemini-flash-latest (recomendado)",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-pro-latest",
            "gemini-2.0-flash"
        ]
        
        ai_provider = st.selectbox(
            "Proveedor",
            ["Auto (fallback)", "OpenAI", "Gemini"],
            index=0,
            key="ai_provider_select",
            help="Auto intenta OpenAI primero, si falla usa Gemini"
        )
        
        # Selector de modelo según proveedor
        if ai_provider == "OpenAI":
            st.session_state["ai_provider"] = "openai"
            selected_model = st.selectbox(
                "Modelo OpenAI",
                openai_models,
                index=0,
                key="openai_model_select"
            )
            # Extraer nombre del modelo (sin el texto adicional)
            model_name = selected_model.split(" ")[0]
            st.session_state["ai_model"] = model_name
            # Debug: mostrar modelo seleccionado
            print(f"✓ Modelo seleccionado: {model_name}")
            
        elif ai_provider == "Gemini":
            st.session_state["ai_provider"] = "gemini"
            selected_model = st.selectbox(
                "Modelo Gemini",
                gemini_models,
                index=0,
                key="gemini_model_select"
            )
            # Extraer nombre del modelo (sin el texto adicional)
            model_name = selected_model.split(" ")[0]
            st.session_state["ai_model"] = model_name
            # Debug: mostrar modelo seleccionado
            print(f"✓ Modelo seleccionado: {model_name}")
            
        else:  # Auto
            st.session_state["ai_provider"] = "auto"
            st.session_state["ai_model"] = None
            st.info("🔄 Modo automático: Intenta OpenAI (gpt-4o-mini) → Gemini (gemini-flash-latest)")
            print("✓ Modo automático activado")
        
        st.markdown("---")
        
        # Progress Tracker
        st.markdown("### 📍 Progreso")
        
        # Verificar estado de formación
        studies_state = st.session_state.get("studies_text_clean")
        has_training_content = studies_state is not None and studies_state != ""
        training_skipped = studies_state == ""
        
        # Definir pasos con estados especiales
        steps = [
            ("1️⃣ Cargar/Crear CV", st.session_state.get("pdf_text_clean") is not None, False),
            ("2️⃣ Formación (opcional)", has_training_content, training_skipped),
            ("3️⃣ CV Maestro", st.session_state.get("cv_master") is not None, False),
            ("4️⃣ Perfil LinkedIn", st.session_state.get("linkedin_profile") is not None, False),
            ("5️⃣ CV Target", st.session_state.get("cv_target") is not None, False),
            ("6️⃣ Análisis ATS", st.session_state.get("ats_analysis") is not None or st.session_state.get("ats_analysis_form") is not None, False),
        ]
        
        for step_name, completed, skipped in steps:
            if completed:
                icon = "✅"
                color = "#27AE60"
                weight = "600"
            elif skipped:
                icon = "➖"  # Guion/menos
                color = "#F39C12"  # Naranja/amarillo
                weight = "600"
            else:
                icon = "⭕"
                color = "#6c757d"
                weight = "500"
            
            st.markdown(f"""
                <div style="padding: 0.5rem 0; color: {color}; font-weight: {weight};">
                    {icon} {step_name}
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Estadísticas
        st.markdown("### 📊 Estadísticas")
        
        # Calcular estadísticas
        cv_count = sum([
            1 if st.session_state.get("cv_master") else 0,
            1 if st.session_state.get("linkedin_profile") else 0,
            1 if st.session_state.get("cv_target") else 0
        ])
        
        # Score ATS
        ats_score = "N/A"
        if st.session_state.get("ats_analysis"):
            ats_score = f"{st.session_state['ats_analysis'].get('score', 0)}/100"
        elif st.session_state.get("ats_analysis_form"):
            ats_score = f"{st.session_state['ats_analysis_form'].get('score', 0)}/100"
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Docs", cv_count, help="Documentos generados")
        with col2:
            st.metric("ATS", ats_score, help="Score de compatibilidad ATS")
        
        st.markdown("---")
        
        # Información y ayuda
        st.markdown("### ℹ️ Información")
        
        with st.expander("📖 Guía Rápida"):
            st.markdown("""
                **Pasos básicos:**
                1. Sube tu CV o créalo desde cero
                2. Genera el CV Maestro
                3. Crea perfil LinkedIn (opcional)
                4. Genera CV Target para un puesto
                5. Analiza compatibilidad ATS
                6. Descarga los PDFs
            """)
        
        with st.expander("🎨 Templates"):
            st.markdown("""
                **Disponibles:**
                - **Clásico**: Formal (ATS ⭐⭐⭐⭐⭐)
                - **Moderno**: Tech/Startups (ATS ⭐⭐⭐⭐)
                - **Minimalista**: Diseño/UX (ATS ⭐⭐⭐⭐)
                - **Creativo**: Marketing (ATS ⭐⭐⭐)
            """)
        
        with st.expander("🔍 Análisis ATS"):
            st.markdown("""
                **🤖 Detección automática:**
                - Entry-level vs Con experiencia
                
                **Criterios adaptativos:**
                
                **Entry-level/Pasantías:**
                - Educación (35%)
                - Proyectos/Habilidades (30%)
                - Palabras clave (25%)
                - Formato (10%)
                
                **Con experiencia:**
                - Experiencia (40%)
                - Palabras clave (30%)
                - Formato (20%)
                - Educación (10%)
                
                **Score objetivo:** 70+ (realista)
            """)
        
        st.markdown("---")
        
        # Links útiles
        st.markdown("### 🔗 Enlaces")
        st.markdown("""
            - [📖 Documentación](https://docs.google.com/presentation/d/1eEIGp8-rix1Tz2_vwm3lCRcLPKQTEXyUOgclLZ90vF0/edit?usp=sharing)
            - [⭐ GitHub](https://github.com/vanerm/cv-alchemist-2.0)
            - [💼 LinkedIn](https://www.linkedin.com/in/vanesamizrahi)
        """)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
            <div style="text-align: center; color: #2C3E50; font-size: 0.8rem; padding: 1rem 0;">
                <p style="margin: 0;">Desarrollado por<br><strong style="color: #667eea;">Vanesa Mizrahi</strong></p>
                <p style="margin-top: 0.5rem; color: #6c757d;">2025</p>
            </div>
        """, unsafe_allow_html=True)


def show_progress_indicator(current_step: int, total_steps: int = 5):
    """Muestra indicador de progreso visual."""
    progress = current_step / total_steps
    st.progress(progress)
    st.caption(f"Paso {current_step} de {total_steps}")


def render_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Renderiza una card informativa."""
    st.markdown(f"""
        <div class="card">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 2rem; margin-right: 1rem;">{icon}</span>
                <h3 style="margin: 0; color: #2C3E50;">{title}</h3>
            </div>
            <div style="color: #6c757d;">
                {content}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = "", icon: str = "📊"):
    """Renderiza una card con métrica."""
    delta_html = f'<div style="color: #27AE60; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>' if delta else ''
    
    st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="color: #6c757d; font-size: 0.9rem; margin-bottom: 0.5rem;">{label}</div>
            <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {value}
            </div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = "", icon: str = ""):
    """Renderiza un header de sección."""
    icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ''
    subtitle_html = f'<p style="color: #6c757d; margin: 0.5rem 0 0 0;">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #2C3E50; margin: 0;">
                {icon_html}{title}
            </h2>
            {subtitle_html}
        </div>
    """, unsafe_allow_html=True)


def render_action_buttons(buttons: list):
    """
    Renderiza botones de acción en columnas.
    
    Args:
        buttons: Lista de diccionarios con 'label', 'key', 'type' (primary/secondary)
    """
    cols = st.columns(len(buttons))
    
    for i, button_config in enumerate(buttons):
        with cols[i]:
            if button_config.get('type') == 'download':
                st.download_button(
                    label=button_config['label'],
                    data=button_config['data'],
                    file_name=button_config['file_name'],
                    mime=button_config.get('mime', 'application/pdf'),
                    key=button_config.get('key')
                )
            else:
                st.button(
                    label=button_config['label'],
                    key=button_config.get('key'),
                    type=button_config.get('type', 'secondary')
                )
