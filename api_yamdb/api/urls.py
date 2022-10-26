from django.urls import include, path
from rest_framework import routers

from api.views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                       CommentViewSet, ReviewViewSet, UserViewSetForAdmin,
                       APIUser, APIToken, APISignUp)


router_v1 = routers.DefaultRouter()

router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSetForAdmin, basename='users')


urlpatterns = [
    path('v1/auth/signup/', APISignUp.as_view(), name='signup'),
    path('v1/auth/token/', APIToken.as_view(), name='token'),
    path('v1/users/me/', APIUser.as_view(), name='me'),
    path('v1/', include(router_v1.urls)),
]
