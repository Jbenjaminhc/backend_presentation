import PyPDF2
from io import BytesIO
import logging
import base64
from PIL import Image

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file):
    """
    Extrae texto y metadatos de un archivo PDF

    Args:
        file: Objeto archivo PDF

    Returns:
        dict: Diccionario con texto extraído, metadatos y referencias a imágenes
    """
    result = {
        'text': '',
        'metadata': {},
        'pages': [],
        'images': []
    }

    try:
        # Manejar diferentes tipos de entrada (FileField, BytesIO, etc.)
        if hasattr(file, 'read'):
            pdf_content = file.read()
            if isinstance(pdf_content, str):
                pdf_content = pdf_content.encode('utf-8')
            pdf_file = BytesIO(pdf_content)
        else:
            pdf_file = BytesIO(file)

        # Abrir el PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extraer metadatos
        if pdf_reader.metadata:
            for key, value in pdf_reader.metadata.items():
                if key.startswith('/'):
                    key = key[1:]
                result['metadata'][key.lower()] = value

        # Extraer texto página por página
        full_text = ""
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            full_text += text + "\n\n"
            result['pages'].append({
                'page_number': i + 1,
                'text': text
            })

        result['text'] = full_text
        return result

    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        result['error'] = str(e)
        return result


def extract_images_from_pdf(file):
    """
    Extrae imágenes de un archivo PDF

    Args:
        file: Objeto archivo PDF

    Returns:
        list: Lista de diccionarios con información de las imágenes extraídas
    """
    # Esta función podría implementarse utilizando bibliotecas como PyMuPDF (fitz)
    # Por simplicidad, devolvemos una lista vacía en este ejemplo
    return []