# src/form_validators.py

"""
Validadores de formulario con regex y seguridad.
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Valida formato de email."""
    if not email or not email.strip():
        return False, "El email es requerido"
    
    email = email.strip()
    
    # Regex para email válido
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Formato de email inválido (ej: nombre@correo.com)"
    
    if len(email) > 254:
        return False, "Email demasiado largo (máx. 254 caracteres)"
    
    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Valida formato de teléfono."""
    if not phone or not phone.strip():
        return True, ""  # Teléfono es opcional
    
    phone = phone.strip()
    
    # Permitir números, espacios, guiones, paréntesis y símbolo +
    pattern = r'^[\d\s\-\+\(\)]+$'
    
    if not re.match(pattern, phone):
        return False, "Teléfono solo puede contener números, +, -, ( )"
    
    # Extraer solo dígitos para validar longitud
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) < 7:
        return False, "Teléfono debe tener al menos 7 dígitos"
    
    if len(digits) > 15:
        return False, "Teléfono demasiado largo (máx. 15 dígitos)"
    
    return True, ""


def validate_name(name: str) -> Tuple[bool, str]:
    """Valida nombre completo."""
    if not name or not name.strip():
        return False, "El nombre completo es requerido"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Nombre debe tener al menos 2 caracteres"
    
    if len(name) > 100:
        return False, "Nombre demasiado largo (máx. 100 caracteres)"
    
    # Permitir letras, espacios, acentos, apóstrofes y guiones
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\'\-]+$'
    
    if not re.match(pattern, name):
        return False, "Nombre solo puede contener letras, espacios, ' y -"
    
    return True, ""


def validate_url(url: str) -> Tuple[bool, str]:
    """Valida formato de URL."""
    if not url or not url.strip():
        return True, ""  # URL es opcional
    
    url = url.strip()
    
    # Regex básico para URL
    pattern = r'^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(/.*)?$'
    
    if not re.match(pattern, url):
        return False, "URL inválida (debe comenzar con http:// o https://)"
    
    if len(url) > 500:
        return False, "URL demasiado larga (máx. 500 caracteres)"
    
    return True, ""


def validate_text_length(text: str, min_len: int = 0, max_len: int = 5000, field_name: str = "Campo") -> Tuple[bool, str]:
    """Valida longitud de texto."""
    if not text or not text.strip():
        if min_len > 0:
            return False, f"{field_name} es requerido"
        return True, ""
    
    text = text.strip()
    
    if len(text) < min_len:
        return False, f"{field_name} debe tener al menos {min_len} caracteres"
    
    if len(text) > max_len:
        return False, f"{field_name} demasiado largo (máx. {max_len} caracteres)"
    
    return True, ""


def sanitize_text(text: str) -> str:
    """Sanitiza texto removiendo caracteres peligrosos."""
    if not text:
        return ""
    
    # Remover caracteres de control excepto saltos de línea y tabs
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Remover múltiples espacios
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def validate_company_name(company: str) -> Tuple[bool, str]:
    """Valida nombre de empresa."""
    if not company or not company.strip():
        return True, ""  # Empresa es opcional en algunos casos
    
    company = company.strip()
    
    if len(company) < 2:
        return False, "Nombre de empresa debe tener al menos 2 caracteres"
    
    if len(company) > 150:
        return False, "Nombre de empresa demasiado largo (máx. 150 caracteres)"
    
    # Permitir letras, números, espacios y caracteres comunes en nombres de empresas
    pattern = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\.\,\&\-\(\)]+$'
    
    if not re.match(pattern, company):
        return False, "Nombre de empresa contiene caracteres no permitidos"
    
    return True, ""


def validate_job_title(title: str) -> Tuple[bool, str]:
    """Valida título de puesto."""
    if not title or not title.strip():
        return True, ""  # Título es opcional en algunos casos
    
    title = title.strip()
    
    if len(title) < 2:
        return False, "Título debe tener al menos 2 caracteres"
    
    if len(title) > 150:
        return False, "Título demasiado largo (máx. 150 caracteres)"
    
    # Permitir letras, números, espacios y caracteres comunes
    pattern = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\/\-\.\,\(\)]+$'
    
    if not re.match(pattern, title):
        return False, "Título contiene caracteres no permitidos"
    
    return True, ""
