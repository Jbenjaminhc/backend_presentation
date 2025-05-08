from celery import shared_task
import logging
from .models import Document, DocumentAnalysis
from .parsers.pdf_parser import extract_text_from_pdf, extract_images_from_pdf
from .parsers.word_parser import extract_text_from_docx
from .parsers.excel_parser import extract_data_from_xlsx

logger = logging.getLogger(__name__)


@shared_task
def process_document(document_id):
    """
    Procesa un documento para extraer su contenido

    Args:
        document_id: ID del documento a procesar

    Returns:
        dict: Resultado del procesamiento
    """
    try:
        document = Document.objects.get(id=document_id)

        # Seleccionar el parser adecuado según el tipo de archivo
        content_data = {}
        if document.file_type == 'PDF':
            content_data = extract_text_from_pdf(document.file)
            images_data = extract_images_from_pdf(document.file)
            content_data['images'] = images_data
        elif document.file_type == 'DOCX':
            content_data = extract_text_from_docx(document.file)
        elif document.file_type == 'XLSX':
            content_data = extract_data_from_xlsx(document.file)
        elif document.file_type == 'TXT':
            # Simple lectura de texto para archivos TXT
            content_data = {
                'text': document.file.read().decode('utf-8'),
                'paragraphs': document.file.read().decode('utf-8').split('\n\n')
            }

        # Crear o actualizar el análisis
        content_text = content_data.get('text', '')
        content_structure = {
            'metadata': content_data.get('metadata', {}),
            'pages': content_data.get('pages', []),
            'paragraphs': content_data.get('paragraphs', []),
            'headings': content_data.get('headings', [])
        }

        analysis, created = DocumentAnalysis.objects.update_or_create(
            document=document,
            defaults={
                'content_text': content_text,
                'content_structure': content_structure,
                'extracted_images': content_data.get('images', []),
                'extracted_tables': content_data.get('tables', []),
                'extracted_charts': content_data.get('chart_data', []),
                'extraction_complete': True
            }
        )

        # Marcar documento como procesado
        document.processed = True
        document.save()

        return {
            'status': 'success',
            'document_id': str(document.id),
            'message': 'Documento procesado con éxito'
        }

    except Document.DoesNotExist:
        logger.error(f"Documento con ID {document_id} no encontrado")
        return {
            'status': 'error',
            'message': f"Documento con ID {document_id} no encontrado"
        }
    except Exception as e:
        logger.error(f"Error procesando documento {document_id}: {str(e)}")

        # Si el documento existe, guardar el error
        try:
            document = Document.objects.get(id=document_id)
            analysis, created = DocumentAnalysis.objects.update_or_create(
                document=document,
                defaults={
                    'processing_errors': str(e),
                    'extraction_complete': False
                }
            )
        except:
            pass

        return {
            'status': 'error',
            'message': f"Error procesando documento: {str(e)}"
        }