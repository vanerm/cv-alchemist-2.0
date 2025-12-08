# src/pdf_validator.py

import pdfplumber
from typing import Tuple, Optional
try:
    from PyPDF2 import PdfReader
    from PyPDF2.errors import PdfReadError
except ImportError:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError


class PDFValidationResult:
    """Resultado de la validación de un PDF."""
    
    def __init__(self, is_valid: bool, error_message: Optional[str] = None, 
                 warning_message: Optional[str] = None, metadata: Optional[dict] = None):
        self.is_valid = is_valid
        self.error_message = error_message
        self.warning_message = warning_message
        self.metadata = metadata or {}


def validate_pdf(file, max_size_mb: int = 10) -> PDFValidationResult:
    """
    Valida un archivo PDF antes de procesarlo.
    
    Args:
        file: Archivo subido por Streamlit (UploadedFile)
        max_size_mb: Tamaño máximo permitido en MB
    
    Returns:
        PDFValidationResult con el resultado de la validación
    """
    
    # 1. Validación de tamaño
    file.seek(0, 2)  # Ir al final del archivo
    file_size = file.tell()
    file.seek(0)  # Volver al inicio
    
    file_size_mb = file_size / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        return PDFValidationResult(
            is_valid=False,
            error_message=f"El archivo es demasiado grande ({file_size_mb:.1f}MB). Máximo permitido: {max_size_mb}MB"
        )
    
    # 2. Validación de tipo de archivo (verificar que sea realmente un PDF)
    file.seek(0)
    header = file.read(5)
    file.seek(0)
    
    if header != b'%PDF-':
        return PDFValidationResult(
            is_valid=False,
            error_message="El archivo no es un PDF válido. Verifica que el archivo no esté corrupto."
        )
    
    # 3. Validación de PDF protegido y estructura
    try:
        file.seek(0)
        pdf_reader = PdfReader(file)
        file.seek(0)
        
        # Verificar si está encriptado
        if pdf_reader.is_encrypted:
            return PDFValidationResult(
                is_valid=False,
                error_message="El PDF está protegido con contraseña. Por favor, desbloquéalo antes de subirlo."
            )
        
        num_pages = len(pdf_reader.pages)
        
    except PdfReadError as e:
        return PDFValidationResult(
            is_valid=False,
            error_message=f"El PDF está corrupto o dañado: {str(e)}"
        )
    except Exception as e:
        return PDFValidationResult(
            is_valid=False,
            error_message=f"Error al leer el PDF: {str(e)}"
        )
    
    # 4. Validación de contenido extraíble
    try:
        file.seek(0)
        with pdfplumber.open(file) as pdf:
            total_text = ""
            for page in pdf.pages:
                text = page.extract_text() or ""
                total_text += text
            
            text_length = len(total_text.strip())
            
            # Si hay muy poco texto, probablemente sea un PDF escaneado
            warning_msg = None
            if text_length < 50:
                warning_msg = (
                    "⚠️ El PDF parece contener muy poco texto extraíble. "
                    "Puede ser una imagen escaneada. Los resultados pueden no ser óptimos."
                )
            
            # Metadata para feedback
            metadata = {
                "num_pages": num_pages,
                "text_length": text_length,
                "file_size_mb": round(file_size_mb, 2)
            }
            
            file.seek(0)
            return PDFValidationResult(
                is_valid=True,
                warning_message=warning_msg,
                metadata=metadata
            )
            
    except Exception as e:
        return PDFValidationResult(
            is_valid=False,
            error_message=f"Error al extraer contenido del PDF: {str(e)}"
        )
