from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .log_info.urls import router as log_info_router

router = DefaultRouter()
router.registry.extend(log_info_router.registry)  # Объединяем роутеры из приложения log_info

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include("api.openapi.urls")),
]
