from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment, Title, Category, Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, title_object):
        rating_title = int(
            Review.objects.filter(title=title_object).aggregate(
                Avg('score'))
        )
        return rating_title

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genres', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, data):
        score = data.get('score')
        if score not in range(1, 11):
            raise serializers.ValidationError(
                ('Оценка произведения должна быть целой цифрой в диапазоне '
                 'от 1 до 10')
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
