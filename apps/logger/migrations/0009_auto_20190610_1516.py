# Generated by Django 2.1.5 on 2019-06-10 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0008_auto_20190610_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='code',
            field=models.CharField(max_length=255, verbose_name='Код ответа'),
        ),
    ]
