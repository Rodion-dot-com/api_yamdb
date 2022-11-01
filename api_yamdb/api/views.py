from functools import partial
from http.client import METHOD_NOT_ALLOWED
from pickle import PUT
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, permissions, viewsets, generics
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api import permissions
from reviews.models import Title, Review, Comment, Genre, Category, User
from api.serializers import (ReviewSerializer, CommentSerializer,
                             CategorySerializer, GenreSerializer,
                             AdminSerializer, UserSerializer, TokenSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('titles_id')
        title = get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('titles_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user,
                        title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


def create_conf_code_and_send_email(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code',
        f'Your confirmation code {confirmation_code}',
        'from@YAMDB.ru',
        (user.email,)
    )


class AuthClass(viewsets.ViewSet):
    """Класс авторизации пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False, methods=['post'],
        url_path='signup', permission_classes=(AllowAny, )
    )
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            create_conf_code_and_send_email(
                serializer.data['username'])
            return Response(
                {'email': serializer.data['email'],
                 'username': serializer.data['username']},
                status=status.HTTP_200_OK)

    @action(
        detail=False, methods=['post'],
        url_path='token', permission_classes=(AllowAny, )
    )
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])
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
    serializer_class = AdminSerializer
    lookup_field = 'username'
    permission_classes = (permissions.AdminPermissions, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

    @action(
        detail=False, methods=['get'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer
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

