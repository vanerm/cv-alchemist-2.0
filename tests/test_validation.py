#!/usr/bin/env python3
"""
Script de prueba para validación de PDFs.
Ejecutar: python test_validation.py
"""

from src.pdf_validator import validate_pdf, PDFValidationResult
from io import BytesIO

def test_invalid_file():
    """Test con archivo no-PDF"""
    fake_file = BytesIO(b"Este no es un PDF")
    fake_file.name = "fake.pdf"
    
    result = validate_pdf(fake_file)
    print(f"Test archivo inválido: {'✓ PASS' if not result.is_valid else '✗ FAIL'}")
    print(f"  Mensaje: {result.error_message}\n")

def test_large_file():
    """Test con archivo muy grande"""
    large_file = BytesIO(b"%PDF-1.4\n" + b"x" * (11 * 1024 * 1024))  # 11MB
    large_file.name = "large.pdf"
    
    result = validate_pdf(large_file, max_size_mb=10)
    print(f"Test archivo grande: {'✓ PASS' if not result.is_valid else '✗ FAIL'}")
    print(f"  Mensaje: {result.error_message}\n")

def test_valid_header():
    """Test con header PDF válido"""
    valid_file = BytesIO(b"%PDF-1.4\n")
    valid_file.name = "valid.pdf"
    
    result = validate_pdf(valid_file)
    print(f"Test header válido: {'✓ PASS' if result.is_valid or 'corrupto' in result.error_message else '✗ FAIL'}")
    print(f"  Mensaje: {result.error_message or 'Header válido detectado'}\n")

if __name__ == "__main__":
    print("=== Pruebas de Validación de PDFs ===\n")
    test_invalid_file()
    test_large_file()
    test_valid_header()
    print("=== Pruebas completadas ===")
