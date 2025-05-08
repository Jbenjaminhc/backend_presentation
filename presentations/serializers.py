from rest_framework import serializers
from .models import Presentation, Slide
from api.serializers import UserSerializer


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ['id', 'title', 'order', 'content', 'template_type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PresentationSerializer(serializers.ModelSerializer):
    owner_details = serializers.SerializerMethodField()
    slides_count = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Presentation
        fields = ['id', 'title', 'description', 'owner', 'owner_details',
                  'created_at', 'updated_at', 'is_public', 'is_template',
                  'theme', 'thumbnail_url', 'slides_count', 'original_document']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at',
                            'thumbnail_url', 'slides_count']

    def get_owner_details(self, obj):
        return {
            'id': obj.owner.id,
            'email': obj.owner.email,
            'full_name': obj.owner.get_full_name()
        }

    def get_slides_count(self, obj):
        return obj.slides.count()

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url') and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None


class PresentationListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listar presentaciones"""
    owner_details = serializers.SerializerMethodField()
    slides_count = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Presentation
        fields = ['id', 'title', 'owner_details', 'created_at',
                  'updated_at', 'thumbnail_url', 'slides_count']

    def get_owner_details(self, obj):
        return {
            'id': obj.owner.id,
            'email': obj.owner.email,
            'full_name': obj.owner.get_full_name()
        }

    def get_slides_count(self, obj):
        return obj.slides.count()

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url') and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None


class PresentationDetailSerializer(PresentationSerializer):
    """Serializer detallado que incluye las diapositivas"""
    slides = SlideSerializer(many=True, read_only=True)

    class Meta(PresentationSerializer.Meta):
        fields = PresentationSerializer.Meta.fields + ['slides']