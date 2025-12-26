from django.db import models
from django.contrib.auth.models import User

from .validators import (
    validate_positive_price,
    validate_no_bad_words,
    validate_min_length_10,
    validate_phone_simple,
)


class PublishedBbManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(price__gt=0)
# -----------------------------
# One-to-Many (ForeignKey)
# -----------------------------
class Rubric(models.Model):
    description = models.CharField(max_length=100, blank=True, default='', verbose_name='Описание')
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Название рубрики'
    )

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------
# One-to-One
# -----------------------------
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_simple],
        verbose_name='Телефон'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'


# -----------------------------
# Many-to-Many
# -----------------------------
class Tag(models.Model):
    color = models.CharField(max_length=20, blank=True, default='', verbose_name='Цвет')
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------
# Основная модель
# -----------------------------
class Bb(models.Model):
    title = models.CharField(
        max_length=50,
        validators=[validate_no_bad_words],
        verbose_name='Заголовок'
    )
    content = models.TextField(
        validators=[validate_min_length_10],
        verbose_name='Описание'
    )
    price = models.FloatField(
        validators=[validate_positive_price],
        verbose_name='Цена'
    )
    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано'
    )

    # One-to-Many
    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Рубрика'
    )

    # Many-to-One (доп. пример FK)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bbs',
        verbose_name='Автор'
    )

    # Many-to-Many
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='bbs',
        verbose_name='Теги'
    )

    constraints = [
        models.CheckConstraint(
            check=models.Q(price__gte=0),
            name='price_non_negative'
        )
    ]

    objects = models.Manager()  # стандартный менеджер
    published_objects = PublishedBbManager()

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']

    def __str__(self):
        return self.title


# -----------------------------
# Many-to-Many through
# -----------------------------
class BbTag(models.Model):
    bb = models.ForeignKey(
        Bb,
        on_delete=models.CASCADE,
        verbose_name='Объявление'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )
    weight = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Вес тега'
    )

    class Meta:
        verbose_name = 'Связь объявление–тег'
        verbose_name_plural = 'Связи объявление–тег'
        unique_together = ('bb', 'tag')

    def __str__(self):
        return f'{self.bb} – {self.tag}'

