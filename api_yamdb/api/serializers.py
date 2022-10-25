from django.db.models import Avg
from rest_framework import serializers, exceptions
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Review, Comment, Title, Category, Genre, User


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
        if type(score) is not int or score not in range(1, 11):
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


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Неверное имя пользователя')
        return value


class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Неверное имя пользователя')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Неверное имя пользователя')
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound('Пользователь не найден')
        return value
