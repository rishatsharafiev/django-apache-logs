# Generated by Django 2.1.5 on 2019-06-10 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0010_auto_20190610_1559'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='log',
            index=models.Index(fields=['uri'], name='uri_idx'),
        ),
        migrations.AddIndex(
            model_name='log',
            index=models.Index(fields=['ip_address'], name='ip_address_idx'),
        ),
    ]
