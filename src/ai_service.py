# src/ai_service.py

"""
Módulo de integración con APIs de IA (OpenAI con fallback a Gemini).

El objetivo es exponer una función simple:

    generate_cv_output(prompt: str) -> str

que reciba un prompt y devuelva texto generado, con fallback automático
si OpenAI falla.

Requisitos:
- Variable de entorno OPENAI_API_KEY (primaria)
- Variable de entorno GEMINI_API_KEY (fallback)
- Paquetes:
    - python-dotenv
    - openai>=1.0.0
    - google-generativeai
"""

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai

# Carga las variables de entorno desde un archivo .env (si existe).
load_dotenv()

# Modelos por defecto
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# Clientes globales reutilizables
_openai_client: Optional[OpenAI] = None
_gemini_configured: bool = False


def _get_openai_client() -> Optional[OpenAI]:
    """
    Devuelve una instancia de cliente de OpenAI.
    Retorna None si no encuentra la API key configurada.
    """
    global _openai_client

    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            _openai_client = OpenAI(api_key=api_key)

    return _openai_client


def _configure_gemini() -> bool:
    """
    Configura el cliente de Gemini.
    Retorna True si se configuró exitosamente.
    """
    global _gemini_configured
    
    if not _gemini_configured:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            _gemini_configured = True
    
    return _gemini_configured


def _generate_with_openai(prompt: str, model: str) -> Optional[str]:
    """
    Intenta generar contenido con OpenAI.
    Retorna el texto generado o None si falla.
    """
    try:
        client = _get_openai_client()
        if not client:
            print("⚠️ OpenAI: No se encontró OPENAI_API_KEY")
            return None

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente experto en redacción profesional. "
                        "Debes seguir EXACTAMENTE las instrucciones del usuario. "
                        "No debes inventar datos, habilidades, experiencia, logros "
                        "ni información no presente en el prompt. "
                        "Mantén un tono profesional, claro y preciso."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.1,
            top_p=1,
            max_tokens=7000,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ OpenAI error: {type(e).__name__}: {str(e)}")
        return None


def _generate_with_gemini(prompt: str, model: str) -> Optional[str]:
    """
    Intenta generar contenido con Gemini.
    Retorna el texto generado o None si falla.
    """
    try:
        if not _configure_gemini():
            print("⚠️ Gemini: No se encontró GEMINI_API_KEY")
            return None

        # Construir prompt completo con instrucciones del sistema
        full_prompt = (
            "Eres un asistente experto en redacción profesional. "
            "Debes seguir EXACTAMENTE las instrucciones del usuario. "
            "No debes inventar datos, habilidades, experiencia, logros "
            "ni información no presente en el prompt. "
            "Mantén un tono profesional, claro y preciso.\n\n"
            f"{prompt}"
        )

        model_instance = genai.GenerativeModel(model)
        
        # Configuración de seguridad más permisiva
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        response = model_instance.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                top_p=1,
                max_output_tokens=7000,
            ),
            safety_settings=safety_settings
        )

        return response.text

    except Exception as e:
        print(f"❌ Gemini error: {type(e).__name__}: {str(e)}")
        return None


def generate_cv_output(prompt: str, model: Optional[str] = None) -> str:
    """
    Genera texto del CV usando IA con fallback automático.
    Intenta primero con OpenAI, si falla usa Gemini.

    Parámetros:
        prompt: Instrucciones completas que describen la tarea a la IA.
        model: Nombre del modelo a utilizar (opcional).

    Retorna:
        Texto generado por el modelo o un mensaje de error amigable.
    """
    # Intentar con OpenAI primero
    openai_model = model or DEFAULT_OPENAI_MODEL
    print(f"🔄 Intentando generar con OpenAI ({openai_model})...")
    result = _generate_with_openai(prompt, openai_model)
    
    if result:
        print("✅ Contenido generado exitosamente con OpenAI")
        return result
    
    # Fallback a Gemini
    gemini_model = DEFAULT_GEMINI_MODEL
    print(f"🔄 OpenAI no disponible, intentando con Gemini ({gemini_model})...")
    result = _generate_with_gemini(prompt, gemini_model)
    
    if result:
        print("✅ Contenido generado exitosamente con Gemini")
        return result
    
    # Si ambos fallan
    return (
        "⚠️ No se pudo generar contenido con ninguna API de IA.\n\n"
        "El sistema intentó usar:\n"
        "1. OpenAI (primaria)\n"
        "2. Gemini (fallback)\n\n"
        "Por favor verifica:\n"
        "- Al menos una API key está configurada (OPENAI_API_KEY o GEMINI_API_KEY)\n"
        "- Los modelos configurados son válidos\n"
        "- Hay conexión a internet\n"
        "- No se excedieron los límites de uso\n"
    )
