# Generated by Django 3.2.16 on 2022-12-16 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='no_answers',
            field=models.BooleanField(null=True, verbose_name='Без ответов'),
        ),
    ]