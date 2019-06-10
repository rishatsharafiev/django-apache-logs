from django.db import models
from django.urls import reverse


class Log(models.Model):
    """Log Model"""

    ip_address = models.CharField(verbose_name='IP адрес', max_length=255)
    created_at = models.DateField(verbose_name='Дата')
    method = models.CharField(verbose_name='HTTP метод', max_length=255)
    uri = models.CharField(verbose_name='URI', max_length=255)
    code = models.CharField(verbose_name='Код ответа', max_length=255)
    size = models.PositiveIntegerField(verbose_name='Размер в байтах')

    def get_absolute_url(self):
        """Get absolute url to entity"""
        return reverse('logger:log-list', kwargs={'pk': self.pk})

    class Meta:
        """Meta"""

        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('-created_at',)

        indexes = [
            models.Index(fields=['-created_at'], name='created_at_idx'),
            models.Index(fields=['uri'], name='uri_idx'),
            models.Index(fields=['ip_address'], name='ip_address_idx'),
        ]
