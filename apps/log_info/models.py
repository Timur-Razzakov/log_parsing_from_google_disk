from django.db import models


# Create your models here.
class Logs(models.Model):
    """Модель для хранения данных из логов"""

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"

    time = models.DateTimeField(verbose_name='Дата и время, указанные в логах')
    remote_ip = models.CharField(max_length=255, verbose_name='Удалённый IP адрес')
    url = models.CharField(max_length=255, verbose_name='Путь запроса')
    method = models.CharField(max_length=255, verbose_name='метод запроса', help_text='GET, POST, PUT..')
    bytes = models.BigIntegerField(default=0, blank=True, null=True, verbose_name='Размер запроса')
    response = models.CharField(max_length=255, verbose_name='Код ответа на запрос')
    user_agent = models.CharField(max_length=255,
                                  verbose_name='Наименование устройства, с которого пришёл запрос')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.url
