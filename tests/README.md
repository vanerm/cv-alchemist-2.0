# 🧪 Tests y Scripts de Debugging

Esta carpeta contiene scripts para testing, debugging y validación del proyecto.

---

## 📋 Scripts Disponibles

### 🔌 `test_apis.py`
**Propósito**: Verificar conectividad con APIs de IA (OpenAI y Gemini)

**Uso**:
```bash
python tests/test_apis.py
```

**Qué hace**:
- Verifica que las API keys estén configuradas
- Prueba conexión con OpenAI
- Prueba conexión con Gemini (fallback)
- Muestra qué modelos están disponibles

**Cuándo usar**: Antes de deployar o cuando tengas problemas de conexión con las APIs

---

### 💾 `test_memory.py`
**Propósito**: Monitorear uso de RAM de la aplicación

**Uso**:
```bash
# Terminal 1
python tests/test_memory.py

# Terminal 2
streamlit run app.py
```

**Qué hace**:
- Monitorea memoria en tiempo real cada 5 segundos
- Registra pico máximo, promedio y mínimo
- Genera recomendaciones para deploy
- Determina si 1 GB es suficiente

**Cuándo usar**: Antes del deploy para verificar requisitos de RAM

**Resultado obtenido**: 183 MB máximo ✅ (suficiente para Streamlit Cloud)

---

### 💾 `memory_monitor.py`
**Propósito**: Widget opcional para mostrar RAM en el sidebar de la app

**Uso**:
```python
# En app.py (opcional)
from tests.memory_monitor import display_memory_widget

with st.sidebar:
    display_memory_widget()
```

**Qué hace**:
- Muestra uso de memoria en tiempo real dentro de la app
- Indicador visual con colores (verde/amarillo/rojo)
- Barra de progreso

**Cuándo usar**: Durante desarrollo para debugging de memoria

---

### 📄 `test_pdf_design.py`
**Propósito**: Probar generación de PDFs con diferentes templates

**Uso**:
```bash
python tests/test_pdf_design.py
```

**Qué hace**:
- Genera PDFs de prueba con cada template
- Verifica que los estilos se apliquen correctamente
- Útil para validar cambios en diseño

**Cuándo usar**: Después de modificar templates o estilos de PDF

---

### ✅ `test_validation.py`
**Propósito**: Probar validadores de formularios

**Uso**:
```bash
python tests/test_validation.py
```

**Qué hace**:
- Prueba validación de emails
- Prueba validación de teléfonos
- Prueba validación de URLs
- Prueba sanitización de texto
- Verifica que los regex funcionen correctamente

**Cuándo usar**: Después de modificar validadores en `form_validators.py`

---

## 🚀 Ejecución Rápida

### Verificar todo antes del deploy:
```bash
# 1. Probar APIs
python tests/test_apis.py

# 2. Verificar validaciones
python tests/test_validation.py

# 3. Probar generación de PDFs
python tests/test_pdf_design.py

# 4. Monitorear memoria (opcional)
python tests/test_memory.py
```

---

## 📊 Resultados de Tests

### ✅ Memoria (última prueba)
- **Máximo**: 183 MB
- **Promedio**: ~165 MB
- **Conclusión**: Suficiente para Streamlit Cloud (1 GB)

### ✅ APIs
- OpenAI: Configurada ✓
- Gemini: Configurada ✓
- Fallback: Funcionando ✓

### ✅ Validaciones
- Email: ✓
- Teléfono: ✓
- URLs: ✓
- Sanitización: ✓

### ✅ PDFs
- Templates: 4 disponibles ✓
- Generación: Funcionando ✓
- Diseño: Profesional ✓

---

## 📝 Notas

- Estos scripts NO se ejecutan en producción
- Son solo para desarrollo y debugging local
- No afectan el funcionamiento de la app
- Requieren `psutil` instalado: `pip install psutil`
