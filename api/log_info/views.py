import json
import mimetypes
import os
from datetime import datetime

import gdown
import requests
from django.http import HttpResponse
from django.utils.timezone import make_aware, get_default_timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, inline_serializer
from loguru import logger
from rest_framework import status, generics, serializers, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.log_info.serializers import LogsSerializer, UrlSerializer
from apps.log_info.models import Logs


def get_url_id(url: str):
    """Получаем из ссылки url_id, для преобразования ссылки для скачивания"""
    file_id = url.split('/d/')[1].split('/')[0]
    # Формирование новой ссылки для скачивания
    download_link = f'https://drive.google.com/uc?id={file_id}&export=download'
    return download_link


def download_file(url: str):
    """Скачиваю файл, определяю его тип и сохраняю с соответствующим расширением."""

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Проблема с скачиванием файла: {e}")
        raise
    content_type = response.headers.get('Content-Type')
    logger.info(f"Content-Type: {content_type}")

    # Определение расширения файла на основе его MIME типа
    extension = mimetypes.guess_extension(content_type.split(';')[0].strip())

    local_filename = 'nginx_logs' + extension
    # из-за того что размер может быть большим, использую stream (чтобы сразу всё не грузил в память)
    with open(local_filename, 'wb') as f:
        # сохраняем порционно, чтобы избежать затора
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_filename


def clean_up(loggers_path: str):
    """Удаляем указанный файл"""
    os.remove(loggers_path)


def save_data(loggers_path: str):
    """Получаем данные и сохраняем их в модель Logs"""
    loggers_line_count = 0
    success_count = 0
    error_count = 0
    logs_to_create = []
    with open(loggers_path, 'r') as file:
        for line in file:
            loggers_line_count += 1
            try:
                log_entry = json.loads(line)
                time = datetime.strptime(log_entry['time'], '%d/%b/%Y:%H:%M:%S %z')
                if time.tzinfo is None:
                    time = get_default_timezone()

                method, url, _ = log_entry['request'].split(' ')
                log = Logs(
                    time=time,
                    remote_ip=log_entry['remote_ip'],
                    url=url,
                    method=method,
                    bytes=log_entry.get('bytes', 0),
                    response=log_entry['response'],
                    user_agent=log_entry['agent']
                )
                logs_to_create.append(log)
                if len(logs_to_create) >= 1000:
                    Logs.objects.bulk_create(logs_to_create)
                    success_count += len(logs_to_create)
                    logs_to_create = []  # Очищаем список
            except Exception as e:
                logger.error(f"Ошибка при обработке строки: {e}")
                error_count += 1
    if logs_to_create:
        Logs.objects.bulk_create(logs_to_create)
        success_count += len(logs_to_create)
    result = {
        'Всего строчек с логами': loggers_line_count,
        'Количество строк с ошибками': error_count,
        'Количество успешно сохранённых': success_count,
    }
    return result


def parsing_data(url: str):
    # преобразовываем ссылку просмотра на ссылку скачивания
    get_url_for_download_data = get_url_id(url)
    # Скачиваем
    loggers_path = download_file(get_url_for_download_data)
    # Парсим и сохраняем
    info_about_save = save_data(loggers_path)
    # Удаленяем файл
    clean_up(loggers_path)
    return info_about_save


class GetUrlViewSet(viewsets.ViewSet):
    """Получаем ссылку на логи"""
    serializer_class = UrlSerializer

    @extend_schema(
        summary='Получаем ссылку на логи, чтобы распарсить их"',
        description='Получаем ссылку на логи"',
        request=UrlSerializer,
        responses={status.HTTP_201_CREATED: inline_serializer(
            name='LogProcessingResponse',
            fields={
                'Всего строчек с логами': serializers.IntegerField(),
                'Количество строк с ошибками': serializers.IntegerField(),
                'Количество успешно сохранённых': serializers.IntegerField()
            }
        )

        }
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['log_link']
        try:
            result = parsing_data(url)
        except Exception as e:
            logger.error(f"Ошибка при скачивании или обработке файла: {e}")
            return Response("Возникли проблемы с вашей ссылкой, проверьте пожалуйста",
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(
        summary='Выводим все сохранённые логи',
        description='Получение списка всех логов с возможностью фильтрации, поиска и сортировки.',
    ),
    create=extend_schema(
        summary='Добавление нового лога',
        description='Создание и добавление нового лога в базу данных.',
    ),
    retrieve=extend_schema(
        summary='Получение лога по ID',
        description='Получение детальной информации о логе по его уникальному идентификатору.',
    ),
    update=extend_schema(
        summary='Обновление лога',
        description='Обновление информации о логе по его уникальному идентификатору.',
    ),
    partial_update=extend_schema(
        summary='Частичное обновление лога',
        description='Частичное обновление информации о логе по его уникальному идентификатору.',
    ),
    destroy=extend_schema(
        summary='Удаление лога',
        description='Удаление лога по его уникальному идентификатору.',
    )
)
class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['time', 'method', 'response']
    search_fields = ['url', 'remote_ip', 'response']
    ordering_fields = ['time', 'bytes', 'response']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Лог успешно удалён'}, status=status.HTTP_204_NO_CONTENT)
