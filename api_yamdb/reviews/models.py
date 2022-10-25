from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, UserManager

GENRE_NAME_MAX_LENGTH = 256
GENRE_SLUG_MAX_LENGTH = 50
CATEGORY_NAME_MAX_LENGTH = 256
CATEGORY_SLUG_MAX_LENGTH = 50


class MyUserManager(UserManager):
    """Сохраняет пользователя только с email.
    Зарезервированное имя использовать нельзя."""
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательное')
        if username == 'me':
            raise ValueError('reserved name not use')
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    username = models.CharField(max_length=150, unique=True, db_index=True)
    objects = MyUserManager()

    REQUIRED_FIELDS = ('email', 'password')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ROLES[2][0]

    @property
    def is_moderator(self):
        return self.role == self.ROLES[1][0]


class Genre(models.Model):
    name = models.TextField(max_length=GENRE_NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=GENRE_SLUG_MAX_LENGTH)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField(max_length=CATEGORY_NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=CATEGORY_SLUG_MAX_LENGTH)

    def __str__(self):
        return self.name


def validate_year(value):
    if value < 1 or value > datetime.now().year:
        raise ValidationError('The year is specified incorrectly')


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(Category, related_name='titles', null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )
