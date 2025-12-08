"""
Widget de monitoreo de memoria para mostrar en Streamlit
"""

import streamlit as st
import psutil
import os

def get_memory_usage():
    """Obtiene el uso de memoria del proceso actual"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    mem_mb = mem_info.rss / (1024 * 1024)
    return mem_mb

def display_memory_widget():
    """Muestra widget de memoria en el sidebar"""
    try:
        mem_mb = get_memory_usage()
        mem_gb = mem_mb / 1024
        
        # Determinar color según uso
        if mem_mb < 512:
            color = "🟢"
            status = "Óptimo"
        elif mem_mb < 800:
            color = "🟡"
            status = "Moderado"
        else:
            color = "🔴"
            status = "Alto"
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💾 Uso de Memoria")
        st.sidebar.metric(
            label=f"{color} {status}",
            value=f"{mem_mb:.0f} MB",
            delta=f"{mem_gb:.2f} GB"
        )
        
        # Barra de progreso
        progress = min(mem_mb / 1024, 1.0)  # Máximo 1 GB
        st.sidebar.progress(progress)
        
        if mem_mb > 800:
            st.sidebar.warning("⚠️ Uso de memoria elevado")
        
    except Exception as e:
        st.sidebar.error(f"Error monitoreando memoria: {e}")
