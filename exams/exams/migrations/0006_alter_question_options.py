# Generated by Django 3.2.16 on 2023-01-07 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0005_alter_question_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-visibility', '-active', 'priority', 'id'], 'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
    ]
