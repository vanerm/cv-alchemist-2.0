# src/ai_service.py

"""
Módulo de integración con la API de IA (OpenAI, por defecto).

El objetivo es exponer una función simple:

    generate_cv_output(prompt: str) -> str

que reciba un prompt y devuelva texto generado, manejando errores
de forma amigable para el lector.

Requisitos:
- Variable de entorno OPENAI_API_KEY definida (por ejemplo en un archivo .env).
- Paquetes:
    - python-dotenv
    - openai>=1.0.0
"""

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

# Carga las variables de entorno desde un archivo .env (si existe).
load_dotenv()

# Modelo por defecto. El lector puede cambiarlo vía variable de entorno.
DEFAULT_MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Cliente global reutilizable.
_client: Optional[OpenAI] = None


def _get_openai_client() -> OpenAI:
    """
    Devuelve una instancia de cliente de OpenAI.
    Lanza un RuntimeError si no encuentra la API key configurada.
    """
    global _client

    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "No se encontró la variable de entorno OPENAI_API_KEY. "
                "El lector debe crear un archivo .env en la raíz del proyecto "
                "y definir OPENAI_API_KEY=su_clave_aquí."
            )

        _client = OpenAI(api_key=api_key)

    return _client


def generate_cv_output(prompt: str, model: Optional[str] = None) -> str:
    """
    Llama a la API de OpenAI para generar texto del CV basado en un prompt.

    Parámetros:
        prompt: Instrucciones completas que describen la tarea a la IA.
        model: Nombre del modelo a utilizar (opcional).
               Si no se indica, se usa DEFAULT_MODEL_NAME.

    Retorna:
        Texto generado por el modelo o un mensaje de error amigable.
    """
    try:
        client = _get_openai_client()
        model_name = model or DEFAULT_MODEL_NAME

        response = client.chat.completions.create(
            model=model_name,
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

        content = response.choices[0].message.content
        return content or "No se recibió contenido de la API de OpenAI."

    except Exception as e:
        return (
            "⚠️ Ocurrió un error al llamar a la API de OpenAI.\n"
            f"Detalle técnico: {e}\n\n"
            "El lector debe verificar:\n"
            "- OPENAI_API_KEY está configurada.\n"
            "- El modelo configurado es válido.\n"
            "- Hay conexión a internet.\n"
        )
