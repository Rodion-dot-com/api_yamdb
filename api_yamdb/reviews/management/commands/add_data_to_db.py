import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews import models

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')

name_path = {
    'Category': os.path.join(DATA_DIR, 'category.csv'),
    'Genre': os.path.join(DATA_DIR, 'genre.csv'),
    'Title': os.path.join(DATA_DIR, 'titles.csv'),
    'TitleGenre': os.path.join(DATA_DIR, 'genre_title.csv'),
    'User': os.path.join(DATA_DIR, 'users.csv'),
    'Review': os.path.join(DATA_DIR, 'review.csv'),
    'Comment': os.path.join(DATA_DIR, 'comments.csv'),
}


class Command(BaseCommand):
    help = 'Adds data to the database'

    def add_categories(self):
        with open(name_path['Category'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for category_data in reader:
                try:
                    new_category = models.Category(
                        id=category_data.get('id'),
                        name=category_data.get('name'),
                        slug=category_data.get('slug')
                    )
                    new_category.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Creation skipped. Unable to create an object {e}'))
                    continue
        self.stdout.write(self.style.SUCCESS('Categories added successfully'))

    def add_genres(self):
        with open(name_path['Genre'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for genre_data in reader:
                try:
                    new_genre = models.Genre(
                        id=genre_data.get('id'),
                        name=genre_data.get('name'),
                        slug=genre_data.get('slug')
                    )
                    new_genre.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Creation skipped. Unable to create an object {e}'))
                    continue
        self.stdout.write(self.style.SUCCESS('Genres added successfully'))

    def add_titles(self):
        with open(name_path['Title'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for title_data in reader:
                try:
                    new_title = models.Title(
                        id=title_data.get('id'),
                        name=title_data.get('name'),
                        year=title_data.get('year'),
                        category=models.Category.objects.get(
                            id=title_data.get('category')))
                    new_title.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Creation skipped. Unable to create an object {e}'))
                    continue
        self.stdout.write(self.style.SUCCESS('Titles added successfully'))

    def add_title_genre(self):
        with open(name_path['TitleGenre'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for title_genre_data in reader:
                try:
                    new_title_genre = models.TitleGenre(
                        id=title_genre_data.get('id'),
                        title=models.Title.objects.get(
                            id=title_genre_data.get('title_id')),
                        genre=models.Genre.objects.get(
                            id=title_genre_data.get('genre_id')
                        )
                    )
                    new_title_genre.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Creation skipped. Unable to create an object {e}'))
                    continue
        self.stdout.write(self.style.SUCCESS(
            'Title Genre relations added successfully'))

    def add_users(self):
        with open(name_path['User'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for user_data in reader:
                try:
                    new_user = models.User(
                        id=user_data.get('id'),
                        username=user_data.get('username'),
                        email=user_data.get('email'),
                        role=user_data.get('role'),
                    )
                    new_user.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Creation skipped. Unable to create an object {e}'))
                    continue
        self.stdout.write(self.style.SUCCESS('Users added successfully'))

    def add_reviews(self):
        with open(name_path['Review'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for review_data in reader:
                try:
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
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Creation skipped. Unable to create an object {e}'))
                    continue
        self.stdout.write(self.style.SUCCESS('Reviews added successfully'))

    def add_comments(self):
        with open(name_path['Comment'], newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for comment_data in reader:
                try:
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
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Creation skipped. Unable to create an object {e}'))
                    continue
        self.stdout.write(self.style.SUCCESS('Comments added successfully'))

    def handle(self, *args, **kwargs):
        self.add_categories()
        self.add_genres()
        self.add_titles()
        self.add_title_genre()
        self.add_users()
        self.add_reviews()
        self.add_comments()
        self.stdout.write(self.style.SUCCESS('Data added successfully'))
