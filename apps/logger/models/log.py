from django.db import models


class Log(models.Model):
    """Log Model"""

    ip_address = models.GenericIPAddressField(verbose_name='IP адрес', protocol='both')
    created_at = models.DateField(verbose_name='Дата')
    method = models.CharField(verbose_name='HTTP метод', max_length=255)
    uri = models.TextField(verbose_name='URI')
    code = models.PositiveIntegerField(verbose_name='Код ответа')
    size = models.PositiveIntegerField(verbose_name='Размер в байтах')

    class Meta:
        """Meta"""

        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('-created_at',)
