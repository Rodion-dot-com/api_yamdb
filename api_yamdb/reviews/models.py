from datetime import MINYEAR, datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

GENRE_NAME_MAX_LENGTH = 256
GENRE_SLUG_MAX_LENGTH = 50
CATEGORY_NAME_MAX_LENGTH = 256
CATEGORY_SLUG_MAX_LENGTH = 50

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = [
    ('user', USER),
    ('moderator', MODERATOR),
    ('admin', ADMIN)
]


class MyUserManager(UserManager):
    """Проверка наличия emai."""

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательное')
        if username == 'me':
            raise ValueError('me использовать нельзя')
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role=ADMIN, **extra_fields):
        return super().create_superuser(
            username, email, password, role=ADMIN, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,  # Исключаем повторение адресов
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER,
        verbose_name='Роль',
    )
    objects = MyUserManager()

    REQUIRED_FIELDS = ('email', 'password')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return any(
            [self.role == ADMIN, self.is_superuser]
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class Genre(models.Model):
    name = models.TextField(max_length=GENRE_NAME_MAX_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=GENRE_SLUG_MAX_LENGTH,
                            verbose_name='Уникальное имя')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField(max_length=CATEGORY_NAME_MAX_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=CATEGORY_SLUG_MAX_LENGTH,
                            verbose_name='Уникальное имя')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


def validate_year(value):
    if value < MINYEAR or value > datetime.now().year:
        raise ValidationError('Год указан неправильно')


class Title(models.Model):
    name = models.TextField(verbose_name='Название')
    year = models.IntegerField(validators=[validate_year],
                               verbose_name='Год выпуска')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    genres = models.ManyToManyField(Genre, through='TitleGenre',
                                    verbose_name='Жанры')
    category = models.ForeignKey(Category, related_name='titles', null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Жанр')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='id Произведения'
    )
    text = models.TextField(
        verbose_name='Содержание ревью',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='id Ревью'
    )
    text = models.TextField(
        verbose_name='Содержание комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
