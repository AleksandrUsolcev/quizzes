# Generated by Django 3.2.16 on 2023-01-05 09:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20230105_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='change_revision',
            field=models.BooleanField(default=False, verbose_name='Менять редакции при сохранении теста, вопросов или вариантов ответов'),
        ),
        migrations.AddField(
            model_name='exam',
            name='timer',
            field=models.PositiveIntegerField(blank=True, help_text='Необязательное поле', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(720)], verbose_name='Время на выполнение (мин.)'),
        ),
    ]
