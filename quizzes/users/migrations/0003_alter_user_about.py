# Generated by Django 3.2.16 on 2022-12-17 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='Обо мне'),
        ),
    ]