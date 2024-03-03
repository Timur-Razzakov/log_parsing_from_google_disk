from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from apps.log_info.models import Logs


class UrlSerializer(serializers.Serializer):
    """
    Сериалайзер для ссылки логов
    """
    log_link = serializers.CharField(
        help_text='Ссылка на гугл диск с логами'
    )

    def validate_log_link(self, value):
        # URLValidator для проверки значения
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError as e:
            raise serializers.ValidationError("Неверный формат URL.") from e
        return value


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'
