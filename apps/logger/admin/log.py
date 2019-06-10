from django.contrib import admin


class LogAdmin(admin.ModelAdmin):
    """Log Admin"""

    list_filter = ('method', 'code',)
    list_display = ('ip_address', 'created_at', 'method', 'uri', 'code', 'size',)
    search_fields = ('ip_address', 'method', 'uri', 'code',)
    list_per_page = 30
