"""Admin"""

from django.contrib import admin

from .log import LogAdmin

from ..models import (
    Log,
)

admin.site.register(Log, LogAdmin)

admin.site.site_header = 'Логгирование'
admin.site.site_title = 'Логгирование'
admin.site.index_title = 'Панель управления'
