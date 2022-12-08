from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class QuizTheme(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    description = models.TextField(
        verbose_name='Краткое описание'
    )
    priority = models.PositiveIntegerField(
        verbose_name='Приоритет',
        default=999,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999)
        ]
    )

    class Meta:
        verbose_name = 'Тематика квизов'
        verbose_name_plural = 'Тематики квизов'
        ordering = ['priority', 'title']

    def __str__(self):
        return f'{self.title}'


class Quiz(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    description = models.TextField(
        verbose_name='Краткое описание'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='quizzes',
        null=True,
        on_delete=models.SET_NULL
    )
    theme = models.ForeignKey(
        QuizTheme,
        verbose_name='Тематика',
        related_name='quizzes',
        null=True,
        on_delete=models.SET_NULL
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )
    show_results = models.BooleanField(
        verbose_name='Отображать пользователю подробные результаты',
        default=True
    )
    shuffle_variants = models.BooleanField(
        verbose_name='Перемешивать варианты ответов, игнорируя приоритет',
        default=True
    )

    class Meta:
        verbose_name = 'Квиз'
        verbose_name_plural = 'Квизы'
        ordering = ['-created']

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    text = models.TextField(
        verbose_name='Вопрос'
    )
    priority = models.PositiveIntegerField(
        verbose_name='Приоритет',
        default=99,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99)
        ]
    )
    quiz = models.ForeignKey(
        Quiz,
        verbose_name='Квиз',
        related_name='questions',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['priority', 'text']

    def __str__(self):
        if len(self.text) > 48:
            return f'{self.text[:48]}...'
        return f'{self.text}'


class Variant(models.Model):
    text = models.TextField(
        verbose_name='Текст варианта ответа'
    )
    priority = models.PositiveIntegerField(
        verbose_name='Приоритет',
        default=99,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99)
        ]
    )
    correct = models.BooleanField(
        verbose_name='Верный ответ',
        default=False
    )
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        related_name='variants',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['priority', 'text']

    def __str__(self):
        if len(self.text) > 48:
            return f'{self.text[:48]}...'
        return f'{self.text}'
