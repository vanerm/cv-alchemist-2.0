"""
Script para monitorear el uso de memoria de la aplicación Streamlit
Ejecutar en paralelo mientras usas la app
"""

import psutil
import time
import os

def get_streamlit_memory():
    """Obtiene el uso de memoria de procesos Streamlit/Python"""
    total_memory = 0
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if 'python' in proc.info['name'].lower() or 'streamlit' in proc.info['name'].lower():
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                total_memory += mem_mb
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory_mb': mem_mb
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return total_memory, processes

def monitor_memory(duration_seconds=300, interval_seconds=5):
    """Monitorea memoria durante un tiempo determinado"""
    print("🔍 Monitoreando uso de memoria...")
    print(f"⏱️  Duración: {duration_seconds}s | Intervalo: {interval_seconds}s")
    print("-" * 70)
    
    max_memory = 0
    measurements = []
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration_seconds:
            total_mb, processes = get_streamlit_memory()
            max_memory = max(max_memory, total_mb)
            measurements.append(total_mb)
            
            elapsed = int(time.time() - start_time)
            print(f"[{elapsed:03d}s] Memoria actual: {total_mb:.2f} MB | Máximo: {max_memory:.2f} MB")
            
            time.sleep(interval_seconds)
    
    except KeyboardInterrupt:
        print("\n⚠️  Monitoreo interrumpido por el usuario")
    
    # Estadísticas finales
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE USO DE MEMORIA")
    print("=" * 70)
    print(f"💾 Memoria máxima utilizada: {max_memory:.2f} MB ({max_memory/1024:.2f} GB)")
    print(f"📈 Memoria promedio: {sum(measurements)/len(measurements):.2f} MB")
    print(f"📉 Memoria mínima: {min(measurements):.2f} MB")
    print(f"📊 Mediciones realizadas: {len(measurements)}")
    
    # Recomendación
    print("\n" + "=" * 70)
    print("💡 RECOMENDACIÓN PARA DEPLOY")
    print("=" * 70)
    
    if max_memory < 512:
        print("✅ Tu app usa MENOS de 512 MB")
        print("   → Streamlit Community Cloud (1 GB) es SUFICIENTE")
    elif max_memory < 1024:
        print("⚠️  Tu app usa entre 512 MB y 1 GB")
        print("   → Streamlit Community Cloud funcionará, pero puede ser justo")
        print("   → Considerá optimizar si es posible")
    else:
        print("❌ Tu app usa MÁS de 1 GB")
        print(f"   → Necesitás al menos {(max_memory/1024):.1f} GB de RAM")
        print("   → Considerá Streamlit Team Plan (2 GB) o optimizar código")
    
    print("=" * 70)

if __name__ == "__main__":
    print("\n🚀 CV Alchemist 2.0 - Monitor de Memoria\n")
    print("📝 INSTRUCCIONES:")
    print("1. Ejecutá este script en una terminal")
    print("2. En otra terminal, ejecutá: streamlit run app.py")
    print("3. Usá la app normalmente (subir PDFs, generar CVs, etc.)")
    print("4. Este script mostrará el uso de memoria en tiempo real")
    print("\nPresioná Ctrl+C para detener el monitoreo en cualquier momento\n")
    
    input("Presioná ENTER cuando la app esté corriendo...")
    
    # Monitorear por 5 minutos (ajustá según necesites)
    monitor_memory(duration_seconds=300, interval_seconds=5)
