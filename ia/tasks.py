from celery import shared_task
import logging
from .models import VoiceInput, AIPrompt, AIGenerationRequest
from .adapters.voice_processor import SpeechToTextProcessor

logger = logging.getLogger(__name__)


@shared_task
def process_voice_input(voice_input_id):
    """
    Procesa una entrada de voz para convertirla en texto

    Args:
        voice_input_id: ID de la entrada de voz a procesar

    Returns:
        dict: Resultado del procesamiento
    """
    try:
        voice_input = VoiceInput.objects.get(id=voice_input_id)

        # Procesar el audio
        processor = SpeechToTextProcessor(voice_input)
        transcription = processor.process()

        if not transcription:
            return {
                'status': 'error',
                'message': 'No se pudo transcribir el audio'
            }

        # Crear un prompt a partir de la transcripción
        prompt = AIPrompt.objects.create(
            user=voice_input.user,
            text=transcription,
            source='VOICE'
        )

        return {
            'status': 'success',
            'voice_input_id': str(voice_input.id),
            'prompt_id': str(prompt.id),
            'transcription': transcription
        }

    except VoiceInput.DoesNotExist:
        logger.error(f"Entrada de voz con ID {voice_input_id} no encontrada")
        return {
            'status': 'error',
            'message': f"Entrada de voz con ID {voice_input_id} no encontrada"
        }
    except Exception as e:
        logger.error(f"Error procesando entrada de voz {voice_input_id}: {str(e)}")

        # Si la entrada de voz existe, actualizar su estado
        try:
            voice_input = VoiceInput.objects.get(id=voice_input_id)
            voice_input.status = 'FAILED'
            voice_input.error_message = str(e)
            voice_input.save()
        except:
            pass

        return {
            'status': 'error',
            'message': f"Error procesando entrada de voz: {str(e)}"
        }


@shared_task
def generate_presentation_from_prompt(generation_request_id):
    """
    Genera una presentación a partir de un prompt

    Args:
        generation_request_id: ID de la solicitud de generación

    Returns:
        dict: Resultado de la generación
    """
    # Esta tarea es bastante compleja y depende de otros componentes del sistema
    # Aquí se implementaría la lógica para generar la presentación con IA
    # Esto podría incluir:
    # 1. Llamadas a APIs de IA (OpenAI, etc.)
    # 2. Procesamiento de la respuesta para estructurar las diapositivas
    # 3. Creación de la presentación en la base de datos

    # Por simplicidad, no implementamos la lógica completa aquí
    pass