from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, title_object):
        rating_title = int(
            Review.objects.filter(title_id=title_object).aggregate(
                Avg('score'))
        )
        return rating_title

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genres', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, data):
        score = data.get('score')
        if type(score) is not int or score not in range(1, 11):
            raise serializers.ValidationError(
                ('Оценка произведения должна быть целой цифрой в диапазоне '
                 'от 1 до 10')
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        field = '__all__'
        model = Comment
