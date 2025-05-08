from rest_framework import serializers
from .models import Document, DocumentAnalysis


class DocumentSerializer(serializers.ModelSerializer):
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    analysis_complete = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'file_type', 'file_type_display',
                  'file_size', 'created_at', 'updated_at', 'processed',
                  'user_email', 'analysis_complete', 'file_url']
        read_only_fields = ['id', 'created_at', 'updated_at', 'processed',
                            'analysis_complete', 'file_url']

    def get_analysis_complete(self, obj):
        try:
            return obj.analysis.extraction_complete
        except DocumentAnalysis.DoesNotExist:
            return False

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url') and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def validate_file(self, value):
        # Validar tamaño del archivo (máximo 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("El archivo no puede superar los 10MB")

        # Validar extensión
        name = value.name.lower()
        if name.endswith('.pdf'):
            file_type = 'PDF'
        elif name.endswith('.docx'):
            file_type = 'DOCX'
        elif name.endswith('.xlsx'):
            file_type = 'XLSX'
        elif name.endswith('.pptx'):
            file_type = 'PPTX'
        elif name.endswith('.txt'):
            file_type = 'TXT'
        else:
            raise serializers.ValidationError(
                "Formato de archivo no soportado. Formatos válidos: PDF, DOCX, XLSX, PPTX, TXT"
            )

        # Guardar el tipo de archivo para usarlo en create
        self.context['file_type'] = file_type
        return value

    def create(self, validated_data):
        # Añadir tamaño del archivo
        validated_data['file_size'] = validated_data['file'].size

        # Añadir tipo de archivo
        validated_data['file_type'] = self.context.get('file_type')

        return super().create(validated_data)


class DocumentAnalysisSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.title', read_only=True)

    class Meta:
        model = DocumentAnalysis
        fields = ['id', 'document', 'document_title', 'content_text',
                  'content_structure', 'extracted_images', 'extracted_tables',
                  'extracted_charts', 'extraction_complete', 'extraction_date',
                  'processing_errors']
        read_only_fields = ['id', 'document', 'extraction_date']