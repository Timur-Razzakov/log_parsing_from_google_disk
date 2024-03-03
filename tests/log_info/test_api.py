import os
import sqlite3
from unittest import mock

import pytest
from django.test import TestCase
from unittest.mock import patch, mock_open
import requests_mock
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from LogParsing import settings
from api.log_info.views import download_file, save_data, get_url_id
from apps.log_info.models import Logs


# Фикстура для создания клиента API
@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_get_url_id():
    url = "https://drive.google.com/file/d/1AbCdEfGh/view?pli=1"
    expected_file_id = "1AbCdEfGh"
    expected_download_link = f"https://drive.google.com/uc?id={expected_file_id}&export=download"
    download_link = get_url_id(url)

    assert download_link == expected_download_link


def test_download_file_success(mocker):
    expected_content = b"""
    {"time": "17/May/2015:08:05:32 +0000", "remote_ip": "93.180.71.3", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"}
    {"time": "17/May/2015:08:05:23 +0000", "remote_ip": "93.180.71.3", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"}
    {"time": "17/May/2015:08:05:24 +0000", "remote_ip": "80.91.33.133", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.17)"}
    """
    expected_extension = ".txt"
    url = "https://drive.google.com/uc?id=1AbCdEfGh&export=downloa"

    # Настройка мока
    mock_response = mocker.Mock()
    mock_response.iter_content.return_value = [expected_content]
    mock_response.headers = {'Content-Type': 'text/plain'}
    mocker.patch('requests.get', return_value=mock_response)

    local_filename = download_file(url)

    assert local_filename.endswith(expected_extension)
    with open(local_filename, 'rb') as f:
        assert f.read() == expected_content

    # Очистка
    os.remove(local_filename)


# Фикстура для создания тестового лога
@pytest.fixture
def test_log(use_test_database):
    return Logs.objects.create(
        time=timezone.now(),
        remote_ip='192.168.1.1',
        url='/test/url',
        method='GET',
        bytes=512,
        response='200',
        user_agent='pytest'
    )


@pytest.mark.django_db
def test_create_log(test_log):
    assert Logs.objects.count() == 1
    assert test_log.remote_ip == '192.168.1.1'
    assert test_log.url == '/test/url'
    assert test_log.method == 'GET'
    assert test_log.bytes == 512
    assert test_log.response == '200'
    assert test_log.user_agent == 'pytest'

    # Проверяем, что поле created_at было автоматически установлено
    assert test_log.created_at is not None

    assert str(test_log) == test_log.url


@pytest.mark.django_db
def test_save_data_with_valid_log(tmp_path):
    log_content = ' {"time": "17/May/2015:08:05:32 +0000", "remote_ip": "93.180.71.3", "remote_user": "-", "request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"}'
    log_file_path = tmp_path / "nginx_logs.log"
    log_file_path.write_text(log_content)

    result = save_data(str(log_file_path))

    assert result['Всего строчек с логами'] == 1
    assert result['Количество строк с ошибками'] == 0
    assert result['Количество успешно сохранённых'] == 1
    assert Logs.objects.count() == 1


@pytest.mark.django_db
def test_destroy_log(client, test_log):
    # Получаем количество логов до удаления
    logs_count_before = Logs.objects.count()

    # URL для удаления лога
    url = reverse('logs_info-detail', kwargs={'pk': test_log.pk})

    # Выполняем запрос на удаление
    response = client.delete(url)

    # Проверяем статус-код ответа
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data == {'message': 'Лог успешно удалён'}
    assert Logs.objects.count() == logs_count_before - 1
