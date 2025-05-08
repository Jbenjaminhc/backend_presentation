import os
import tempfile
import logging
import json
import requests
import base64
from django.conf import settings

logger = logging.getLogger(__name__)


class SpeechToTextProcessor:
    """
    Procesador para convertir audio a texto
    """

    def __init__(self, voice_input):
        """
        Inicializa el procesador con una entrada de voz
        """
        self.voice_input = voice_input

    def process(self):
        """
        Procesa el audio y devuelve la transcripción
        """
        # Marcar como en procesamiento
        self.voice_input.status = 'PROCESSING'
        self.voice_input.save()

        try:
            # Obtener el audio
            audio_file = self.voice_input.audio_file

            # Determinar el método de procesamiento según el tipo de archivo
            file_ext = os.path.splitext(audio_file.name)[1].lower()

            if file_ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                # Usar servicio de transcripción
                transcription = self._transcribe_audio()
            else:
                raise ValueError(f"Formato de audio no soportado: {file_ext}")

            # Actualizar el modelo con la transcripción
            self.voice_input.transcription = transcription
            self.voice_input.status = 'COMPLETED'
            self.voice_input.save()

            return transcription

        except Exception as e:
            logger.error(f"Error procesando audio: {str(e)}")
            self.voice_input.status = 'FAILED'
            self.voice_input.error_message = str(e)
            self.voice_input.save()
            return None

    def _transcribe_audio(self):
        """
        Transcribe el audio utilizando un servicio externo (ejemplo con OpenAI Whisper API)
        """
        # En un entorno real, aquí se usaría la API de OpenAI o similar
        # Por simplicidad, simulamos una respuesta exitosa

        # Ejemplo de integración con OpenAI Whisper (código comentado)
        """
        import openai

        openai.api_key = settings.OPENAI_API_KEY

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in self.voice_input.audio_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "rb") as audio_file:
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=self.voice_input.language
                )

                transcription = response.get("text", "")
                return transcription
        finally:
            # Limpiar el archivo temporal
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        """

        # Para simular, devolvemos un texto de ejemplo basado en el nombre del archivo
        file_name = os.path.basename(self.voice_input.audio_file.name).lower()

        if "presentacion" in file_name or "presentación" in file_name:
            return "Crea una presentación sobre estrategias de marketing digital con enfoque en redes sociales para 2025. Incluye estadísticas recientes y tendencias emergentes."
        elif "informe" in file_name:
            return "Genera una presentación para el informe trimestral de ventas con gráficos comparativos entre los últimos tres trimestres."
        else:
            return "Crea una presentación de 10 diapositivas sobre inteligencia artificial y su impacto en los negocios modernos."

        # En un caso real, se devolvería la transcripción real del servicio