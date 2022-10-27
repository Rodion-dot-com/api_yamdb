from django.db.models import Avg
from rest_framework import exceptions, serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


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
        return Review.objects.filter(title=title_object).aggregate(
            Avg('score')).get('score__avg')

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
