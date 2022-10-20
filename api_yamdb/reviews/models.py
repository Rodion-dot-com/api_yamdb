from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

GENRE_NAME_MAX_LENGTH = 256
GENRE_SLUG_MAX_LENGTH = 50
CATEGORY_NAME_MAX_LENGTH = 256
CATEGORY_SLUG_MAX_LENGTH = 50


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=30,
    )


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
