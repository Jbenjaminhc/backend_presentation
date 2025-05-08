from rest_framework import serializers
from .models import AIPrompt, VoiceInput, AIGenerationRequest


class AIPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPrompt
        fields = ['id', 'text', 'source', 'created_at']
        read_only_fields = ['id', 'created_at']


class VoiceInputSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = VoiceInput
        fields = ['id', 'audio_file', 'audio_url', 'duration', 'language',
                  'status', 'created_at', 'transcription', 'error_message']
        read_only_fields = ['id', 'duration', 'status', 'created_at',
                            'transcription', 'error_message', 'audio_url']

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio_file and hasattr(obj.audio_file, 'url') and request:
            return request.build_absolute_uri(obj.audio_file.url)
        return None


class AIGenerationRequestSerializer(serializers.ModelSerializer):
    prompt_text = serializers.CharField(write_only=True, required=True)
    document_id = serializers.UUIDField(write_only=True, required=False)
    result_presentation_id = serializers.SerializerMethodField()
    prompt_details = serializers.SerializerMethodField()

    class Meta:
        model = AIGenerationRequest
        fields = ['id', 'prompt_text', 'document_id', 'status', 'created_at',
                  'completed_at', 'result_presentation_id', 'error_message',
                  'prompt_details']
        read_only_fields = ['id', 'status', 'created_at', 'completed_at',
                            'result_presentation_id', 'error_message', 'prompt_details']

    def get_result_presentation_id(self, obj):
        if obj.result_presentation:
            return str(obj.result_presentation.id)
        return None

    def get_prompt_details(self, obj):
        return {
            'id': str(obj.prompt.id),
            'text': obj.prompt.text,
            'source': obj.prompt.source
        }

    def create(self, validated_data):
        user = self.context['request'].user
        prompt_text = validated_data.pop('prompt_text')
        document_id = validated_data.pop('document_id', None)

        # Crear el prompt
        prompt = AIPrompt.objects.create(
            user=user,
            text=prompt_text,
            source='TEXT'  # Por defecto es entrada de texto
        )

        # Buscar el documento si se especificó
        document = None
        if document_id:
            from documents.models import Document
            try:
                document = Document.objects.get(id=document_id, user=user)
            except Document.DoesNotExist:
                pass

        # Crear la solicitud de generación
        request = AIGenerationRequest.objects.create(
            user=user,
            prompt=prompt,
            document=document,
            **validated_data
        )

        # Aquí se podría iniciar el proceso de generación con Celery
        # Por ejemplo: generate_presentation.delay(str(request.id))

        return request