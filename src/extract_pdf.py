import pdfplumber
from typing import List


def extract_text_from_pdf(file) -> str:
    """
    Extrae texto desde un único archivo PDF subido por Streamlit (UploadedFile).
    Devuelve un string con todo el texto del PDF.
    """
    try:
        with pdfplumber.open(file) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text() or ""
                pages_text.append(text)
            return "\n".join(pages_text)

    except Exception as e:
        return f"ERROR_PDF_EXTRACTION: {e}"


def extract_text_from_multiple_pdfs(files: List) -> str:
    """
    Recibe una lista de PDFs subidos por Streamlit y devuelve
    un único string concatenado, separando cada documento con delimitadores.
    """
    all_text = []

    for f in files:
        try:
            text = extract_text_from_pdf(f)

            all_text.append(f"\n--- INICIO_DOCUMENTO: {f.name} ---\n")
            all_text.append(text)
            all_text.append(f"\n--- FIN_DOCUMENTO: {f.name} ---\n")

        except Exception as e:
            all_text.append(f"\nERROR_PDF_EXTRACTION: {f.name} | {e}\n")

    return "\n".join(all_text)
