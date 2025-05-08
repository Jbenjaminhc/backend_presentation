from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoiceInputViewSet, AIPromptViewSet, AIGenerationRequestViewSet

router = DefaultRouter()
router.register(r'voice-inputs', VoiceInputViewSet, basename='voice-input')
router.register(r'prompts', AIPromptViewSet, basename='prompt')
router.register(r'generation-requests', AIGenerationRequestViewSet, basename='generation-request')

urlpatterns = [
    path('', include(router.urls)),
]