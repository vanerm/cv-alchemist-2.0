#!/usr/bin/env python3
"""
Script para testear las API keys de OpenAI y Gemini.
Ejecutar: python test_apis.py
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

def test_openai():
    """Testea la API de OpenAI."""
    print("\n" + "="*60)
    print("🧪 TESTEANDO OPENAI API")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    if not api_key:
        print("❌ OPENAI_API_KEY no configurada")
        return False
    
    print(f"✓ API Key encontrada: {api_key[:20]}...")
    print(f"✓ Modelo: {model}")
    
    try:
        client = OpenAI(api_key=api_key)
        print("🔄 Enviando petición de prueba...")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Di solo: OpenAI funciona correctamente"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ OPENAI FUNCIONA")
        print(f"📝 Respuesta: {result}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        return False


def test_gemini():
    """Testea la API de Gemini."""
    print("\n" + "="*60)
    print("🧪 TESTEANDO GEMINI API")
    print("="*60)
    
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    if not api_key:
        print("❌ GEMINI_API_KEY no configurada")
        return False
    
    print(f"✓ API Key encontrada: {api_key[:20]}...")
    print(f"✓ Modelo: {model}")
    
    try:
        genai.configure(api_key=api_key)
        print("🔄 Enviando petición de prueba...")
        
        model_instance = genai.GenerativeModel(model)
        
        # Configuración de seguridad más permisiva
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        response = model_instance.generate_content(
            "Di solo: Gemini funciona correctamente",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=50,
            ),
            safety_settings=safety_settings
        )
        
        result = response.text
        print(f"✅ GEMINI FUNCIONA")
        print(f"📝 Respuesta: {result}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        return False


def main():
    """Ejecuta todos los tests."""
    print("\n" + "🔬 INICIANDO TESTS DE APIs DE IA ".center(60, "="))
    
    openai_ok = test_openai()
    gemini_ok = test_gemini()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*60)
    print(f"OpenAI: {'✅ FUNCIONA' if openai_ok else '❌ FALLA'}")
    print(f"Gemini: {'✅ FUNCIONA' if gemini_ok else '❌ FALLA'}")
    
    if openai_ok and gemini_ok:
        print("\n🎉 Ambas APIs funcionan correctamente!")
        print("💡 El sistema usará OpenAI primero y Gemini como fallback")
    elif openai_ok:
        print("\n⚠️  Solo OpenAI funciona. Gemini no está disponible como fallback")
    elif gemini_ok:
        print("\n⚠️  Solo Gemini funciona. OpenAI no está disponible")
    else:
        print("\n❌ Ninguna API funciona. Verifica tus API keys")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
