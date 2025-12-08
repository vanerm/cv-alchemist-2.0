#!/usr/bin/env python3
"""
Script de prueba para el diseño mejorado de PDFs.
Genera un CV de ejemplo con todas las mejoras visuales.

Ejecutar: python3 test_pdf_design.py
"""

from src.pdf_generator import generate_pdf

# Contenido de ejemplo con todas las secciones
cv_content = """
Vanesa Mizrahi | vanesamizrahi@gmail.com | +54 9 11 1234-5678 | Buenos Aires, Argentina
iOS Mobile Developer | Estudiante de Data Science
www.linkedin.com/in/vanesamizrahi

**Resumen Profesional**
Desarrolladora de Software (iOS) con experiencia en Análisis Exploratorio (EDA), Visualización y Machine Learning aplicado a problemas reales. Mi enfoque combina programación, estadística, diseño de visualizaciones y comunicación clara de resultados. Actualmente potencio mi perfil técnico con la Diplomatura en Data Science y formación en herramientas de visualización y análisis de datos.

**Experiencia Profesional**
**Mercado Libre — Software Developer**
Buenos Aires, Argentina · 09/2021 – Actualidad
• Desarrollo de aplicaciones móviles iOS con Swift y SwiftUI
• Implementación de arquitecturas MVVM y Clean Architecture
• Integración con APIs REST y servicios backend
• Colaboración en equipo ágil con metodología Scrum
• Code review y mentoring de desarrolladores junior

**Globant — iOS Developer**
Buenos Aires, Argentina · 03/2020 – 08/2021
• Desarrollo de features para aplicaciones bancarias
• Implementación de seguridad y encriptación de datos
• Testing unitario y de integración con XCTest
• Optimización de performance y consumo de memoria

**Educación**
Diplomatura en Data Science · CoderHouse
03/2024 – En curso
Especialización en análisis de datos, machine learning y visualización

Licenciatura en Sistemas · Universidad de Buenos Aires
03/2016 – 12/2020
Promedio: 8.5/10

**Proyectos Relevantes**
▶ **CV Alchemist 2.0**
Aplicación web con IA para crear y optimizar CVs usando Streamlit y OpenAI API. Implementa prompts anti-alucinaciones y validación avanzada de PDFs.
https://github.com/vanerm/cv-alchemist-2.0

▶ **Dashboard de Análisis de Ventas**
Dashboard interactivo en Power BI para análisis de métricas de ventas. Incluye visualizaciones dinámicas y KPIs automatizados.

▶ **Modelo de Predicción de Churn**
Modelo de ML para predecir abandono de clientes usando Python, scikit-learn y pandas. Accuracy: 87%.

**Habilidades**
• Lenguajes: Python, Swift, SQL, R
• Data Science: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
• Visualización: Power BI, Tableau, Plotly
• Mobile: iOS, SwiftUI, UIKit, Xcode
• Herramientas: Git, GitHub, Jupyter, Streamlit
• Metodologías: Scrum, Agile, TDD
"""

def main():
    print("=== Generando PDF de Prueba con Diseño Mejorado ===\n")
    
    try:
        # Generar PDF
        print("📄 Generando PDF...")
        pdf_bytes = generate_pdf(cv_content, "CV Vanesa Mizrahi - Test")
        
        # Guardar archivo
        output_file = "test_cv_design.pdf"
        with open(output_file, "wb") as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF generado exitosamente: {output_file}")
        print(f"📊 Tamaño: {len(pdf_bytes) / 1024:.1f} KB")
        print("\n🎨 Características del diseño:")
        print("  • Tipografía profesional con jerarquía clara")
        print("  • Paleta de colores azul + grises")
        print("  • Líneas divisorias en secciones")
        print("  • Bullets con color acento")
        print("  • Layout optimizado con Platypus")
        print("\n👉 Abre el archivo para ver el resultado")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
