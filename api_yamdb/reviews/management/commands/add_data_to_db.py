import csv
import os

from django.core.management.base import BaseCommand
from reviews import models

from api_yamdb.settings import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, 'static', 'data')

name_path = {
    'category': os.path.join(DATA_DIR, 'category.csv'),
    'genre': os.path.join(DATA_DIR, 'genre.csv'),
    'titles': os.path.join(DATA_DIR, 'titles.csv'),
    'genre_title': os.path.join(DATA_DIR, 'genre_title.csv'),
    'users': os.path.join(DATA_DIR, 'users.csv'),
    'review': os.path.join(DATA_DIR, 'review.csv'),
    'comments': os.path.join(DATA_DIR, 'comments.csv'),
}


class Command(BaseCommand):
    help = 'Adds data to the database'

    def add_categories(self):
        with open(name_path['category'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for category_data in reader:
                new_category = models.Category(
                    id=category_data.get('id'),
                    name=category_data.get('name'),
                    slug=category_data.get('slug')
                )
                new_category.save()
        self.stdout.write('Categories added successfully')

    def add_genres(self):
        with open(name_path['genre'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for genre_data in reader:
                new_genre = models.Genre(
                    id=genre_data.get('id'),
                    name=genre_data.get('name'),
                    slug=genre_data.get('slug')
                )
                new_genre.save()
        self.stdout.write('Genres added successfully')

    def add_titles(self):
        with open(name_path['titles'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for title_data in reader:
                new_title = models.Title(
                    id=title_data.get('id'),
                    name=title_data.get('name'),
                    year=title_data.get('year'),
                    category=models.Category.objects.get(
                        id=title_data.get('category')))
                new_title.save()
        self.stdout.write('Titles added successfully')

    def add_title_genre(self):
        with open(name_path['genre_title'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for title_genre_data in reader:
                new_title_genre = models.TitleGenre(
                    id=title_genre_data.get('id'),
                    title=models.Title.objects.get(
                        id=title_genre_data.get('title_id')),
                    genre=models.Genre.objects.get(
                        id=title_genre_data.get('genre_id')
                    )
                )
                new_title_genre.save()
        self.stdout.write('Title Genre relations added successfully')

    def add_users(self):
        with open(name_path['users'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for user_data in reader:
                new_user = models.User(
                    id=user_data.get('id'),
                    username=user_data.get('username'),
                    email=user_data.get('email'),
                    role=user_data.get('role'),
                )
                new_user.save()
        self.stdout.write('Users added successfully')

    def add_reviews(self):
        with open(name_path['review'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for review_data in reader:
                new_review = models.Review(
                    id=review_data.get('id'),
                    title=models.Title.objects.get(
                        id=review_data.get('title_id')),
                    text=review_data.get('text'),
                    author=models.User.objects.get(
                        id=review_data.get('author')),
                    score=review_data.get('score'),
                    pub_date=review_data.get('pub_date'),
                )
                new_review.save()
        self.stdout.write('Reviews added successfully')

    def add_comments(self):
        with open(name_path['comments'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for comment_data in reader:
                new_comment = models.Comment(
                    id=comment_data.get('id'),
                    review=models.Review.objects.get(
                        id=comment_data.get('review_id')),
                    text=comment_data.get('text'),
                    author=models.User.objects.get(
                        id=comment_data.get('author')),
                    pub_date=comment_data.get('pub_date'),
                )
                new_comment.save()
        self.stdout.write('Comments added successfully')

    def handle(self, *args, **kwargs):
        self.add_categories()
        self.add_genres()
        self.add_titles()
        self.add_title_genre()
        self.add_users()
        self.add_reviews()
        self.add_comments()
        self.stdout.write('Data added successfully')
