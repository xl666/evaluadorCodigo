# Generated by Django 5.0.3 on 2024-03-06 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluador_codigo', '0003_auto_20190209_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
