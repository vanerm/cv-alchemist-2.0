import pdfplumber
from typing import List, Tuple, Optional
from .pdf_validator import validate_pdf, PDFValidationResult


def extract_text_from_pdf(file, validate: bool = True) -> Tuple[Optional[str], Optional[PDFValidationResult]]:
    """
    Extrae texto desde un único archivo PDF subido por Streamlit (UploadedFile).
    
    Args:
        file: Archivo PDF subido
        validate: Si True, valida el PDF antes de extraer
    
    Returns:
        Tuple (texto_extraido, resultado_validacion)
        - texto_extraido: String con el texto o None si hay error
        - resultado_validacion: PDFValidationResult con metadata
    """
    # Validar PDF si está habilitado
    if validate:
        validation_result = validate_pdf(file)
        if not validation_result.is_valid:
            return None, validation_result
    else:
        validation_result = None
    
    try:
        file.seek(0)
        with pdfplumber.open(file) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text() or ""
                pages_text.append(text)
            
            extracted_text = "\n".join(pages_text)
            return extracted_text, validation_result

    except Exception as e:
        return None, PDFValidationResult(
            is_valid=False,
            error_message=f"Error al extraer texto: {str(e)}"
        )


def extract_text_from_multiple_pdfs(files: List, validate: bool = True) -> Tuple[Optional[str], List[PDFValidationResult]]:
    """
    Recibe una lista de PDFs subidos por Streamlit y devuelve
    un único string concatenado, separando cada documento con delimitadores.
    
    Args:
        files: Lista de archivos PDF
        validate: Si True, valida cada PDF antes de extraer
    
    Returns:
        Tuple (texto_concatenado, lista_validaciones)
    """
    all_text = []
    validation_results = []

    for f in files:
        text, validation = extract_text_from_pdf(f, validate=validate)
        validation_results.append(validation)
        
        if text:
            all_text.append(f"\n--- INICIO_DOCUMENTO: {f.name} ---\n")
            all_text.append(text)
            all_text.append(f"\n--- FIN_DOCUMENTO: {f.name} ---\n")
        else:
            error_msg = validation.error_message if validation else "Error desconocido"
            all_text.append(f"\n--- ERROR en {f.name}: {error_msg} ---\n")

    final_text = "\n".join(all_text) if all_text else None
    return final_text, validation_results
