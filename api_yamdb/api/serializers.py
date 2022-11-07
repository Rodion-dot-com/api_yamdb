from rest_framework import exceptions, serializers
from rest_framework.relations import SlugRelatedField
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
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True, source='genres')
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = ('name', 'year', 'description')
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
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        if self.context.get('request').method != 'POST':
            return attrs
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('titles_id')
        if Review.objects.filter(title__id=title_id, author=author).exists():
            raise serializers.ValidationError(
                'На каждое произведение можно оставить только одно ревью')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Неверное имя пользователя')
        return value


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email')

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
