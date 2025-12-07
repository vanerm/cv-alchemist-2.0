# src/extract_pdf.py

import io
from typing import Optional
import pdfplumber


class PDFExtractionError(Exception):
    """Errores específicos al procesar el PDF."""
    pass


def validate_pdf(file) -> None:
    """
    Valida que el archivo subido sea un PDF razonable.
    Lanza PDFExtractionError con mensajes claros si algo falla.
    """
    if file is None:
        raise PDFExtractionError("No se recibió ningún archivo.")

    # En Streamlit, file.type suele ser "application/pdf"
    content_type = getattr(file, "type", None)
    if content_type != "application/pdf":
        raise PDFExtractionError("El archivo debe ser un PDF con extensión .pdf.")

    # Tamaño mínimo razonable (por ejemplo > 1 KB)
    file_size = getattr(file, "size", None)
    if file_size is not None and file_size < 1024:
        raise PDFExtractionError(
            "El PDF parece estar vacío o dañado (tamaño demasiado pequeño)."
        )


def extract_text_from_pdf(file) -> str:
    """
    Extrae el texto de un PDF usando pdfplumber.
    Devuelve un string con el texto completo.
    """
    try:
        # Leer los bytes del archivo subido (Streamlit da un buffer en memoria)
        file_bytes = file.read()
        if not file_bytes:
            raise PDFExtractionError("No se pudo leer el contenido del PDF.")

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages_text = []
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                pages_text.append(page_text)

        full_text = "\n".join(pages_text).strip()

        if not full_text:
            raise PDFExtractionError(
                "No se pudo extraer texto del PDF. "
                "Puede ser un PDF escaneado (solo imágenes) o protegido."
            )

        return full_text

    except PDFExtractionError:
        # Re-lanzar si ya es un error controlado
        raise
    except Exception as e:
        raise PDFExtractionError(f"Error inesperado al procesar el PDF: {e}")


def clean_text(text: Optional[str]) -> str:
    """
    Limpia y normaliza el texto extraído.
    Esta función se puede ir refinando más adelante.
    """
    if not text:
        return ""

    # Unificar saltos de línea
    cleaned = text.replace("\r", "\n")

    # Quitar espacios extra y líneas vacías
    lines = [line.strip() for line in cleaned.split("\n")]
    non_empty_lines = [line for line in lines if line]

    return "\n".join(non_empty_lines)
