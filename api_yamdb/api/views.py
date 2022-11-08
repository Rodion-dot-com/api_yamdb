from api.filtersets import TitleFilter
from api.permissions import (AdminPermissions, AllWithoutGuestOrReadOnly,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer,
                             TitleCreateUpdateDestroySerializer,
                             TitleReadSerializer, TokenSerializer,
                             UserSerializer)
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AllWithoutGuestOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('titles_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('titles_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user,
                        title=title)

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AllWithoutGuestOrReadOnly, )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('titles_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title__id=title_id)
        serializer.save(author=self.request.user, review=review)

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in {'list', 'retrieve'}:
            return TitleReadSerializer
        return TitleCreateUpdateDestroySerializer


def create_conf_code_and_send_email(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        (user.email,)
    )


class AuthClass(viewsets.ViewSet):
    """Класс авторизации пользователей."""

    @action(
        detail=False, methods=('post',),
        url_path='signup', permission_classes=(AllowAny, )
    )
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            raise ValidationError(
                'Пользователь с такими данными уже существует')
        create_conf_code_and_send_email(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)

    @action(
        detail=False, methods=('post',),
        url_path='token', permission_classes=(AllowAny, )
    )
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.data['username'])
        if default_token_generator.check_token(
           user, serializer.data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK)
        return Response({
            'confirmation code': 'Некорректный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AdminPermissions, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

    @action(
        detail=False, methods=('get',),
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,),
    )
    def about_me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @about_me.mapping.patch
    def patch_about_me(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
