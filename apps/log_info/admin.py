from django.contrib import admin

from apps.log_info.models import Logs


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('time', 'remote_ip', 'url', 'method', 'bytes', 'response', 'user_agent', 'created_at')
    list_filter = ('time', 'method', 'response')
    search_fields = ('url', 'remote_ip', 'method', 'response')
