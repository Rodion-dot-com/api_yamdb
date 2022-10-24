from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment, Title, Category, Genre, TitleGenre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')
    genre = GenreSerializer(read_only=True, many=True, source='genres')
    category = CategorySerializer(read_only=True)

    def get_rating(self, title_object):
        rating_title = Review.objects.filter(title=title_object).aggregate(
                Avg('score')).get('score__avg')
        return rating_title

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleCreateUpdateDestroySerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(many=True, source='genres', slug_field='slug',
                             queryset=Genre.objects.all())
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        read_only_fields = ('id',)
        model = Title

    def create(self, validated_data):
        genre_list = validated_data.pop('genres')

        title = Title.objects.create(
            **validated_data
        )

        for genre in genre_list:
            TitleGenre.objects.create(
                title=title,
                genre=genre,
            )

        return title


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
