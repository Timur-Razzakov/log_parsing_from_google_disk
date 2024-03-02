from django.test import TestCase
from django.utils import timezone
from .models import Logs


class LogsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем запись для тестирования
        Logs.objects.create(
            time=timezone.now(),
            remote_ip='192.168.1.1',
            url='/test/url',
            method='GET',
            bytes=1024,
            response='200 OK',
            user_agent='UnitTestAgent'
        )

    def test_time_label(self):
        log = Logs.objects.get(id=1)
        field_label = log._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'Дата и время, указанные в логах')

    def test_remote_ip_label(self):
        log = Logs.objects.get(id=1)
        field_label = log._meta.get_field('remote_ip').verbose_name
        self.assertEquals(field_label, 'Удалённый IP адрес')

    def test_url_label(self):
        log = Logs.objects.get(id=1)
        field_label = log._meta.get_field('url').verbose_name
        self.assertEquals(field_label, 'Путь запроса')

    def test_method_label(self):
        log = Logs.objects.get(id=1)
        field_label = log._meta.get_field('method').verbose_name
        self.assertEquals(field_label, 'метод запроса')

    def test_bytes_label(self):
        log = Logs.objects.get(id=1)
        field_label = log._meta.get_field('bytes').verbose_name
        self.assertEquals(field_label, 'Размер запроса')

    def test_response_label(self):
        log = Logs.objects.get(id=1)
        field_label = log._meta.get_field('response').verbose_name
        self.assertEquals(field_label, 'Код ответа на запрос')

    def test_user_agent_label(self):
        log = Logs.objects.get(id=1)
        field_label = log._meta.get_field('user_agent').verbose_name
        self.assertEquals(field_label, 'Наименование устройства, с которого пришёл запрос')

    def test_created_at_auto_now_add(self):
        log = Logs.objects.get(id=1)
        self.assertTrue(isinstance(log.created_at, timezone.datetime))

    def test_object_name_is_url(self):
        log = Logs.objects.get(id=1)
        expected_object_name = log.url
        self.assertEquals(expected_object_name, str(log))
