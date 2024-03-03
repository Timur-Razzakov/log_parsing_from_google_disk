from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.log_info.views import GetUrlViewSet, LogsViewSet

router = DefaultRouter()
router.register(r'logs_info', LogsViewSet, basename='logs_info')
router.register(r'send_url', GetUrlViewSet, basename='send-url')
urlpatterns = [
    # path("send_url/", GetUrl.as_view()),
    path("", include(router.urls)),
]
