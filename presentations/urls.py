from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import PresentationViewSet, SlideViewSet

router = DefaultRouter()
router.register(r'presentations', PresentationViewSet, basename='presentation')

# Rutas anidadas para diapositivas dentro de presentaciones
slides_router = NestedSimpleRouter(router, r'presentations', lookup='presentation')
slides_router.register(r'slides', SlideViewSet, basename='presentation-slides')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(slides_router.urls)),
]