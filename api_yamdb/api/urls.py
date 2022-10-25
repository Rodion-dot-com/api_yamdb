from django.urls import include, path
from rest_framework import routers

from api.views import (GenreViewSet, CategoryViewSet, UserViewSetForAdmin,
                       APIUser, APIToken, APISignUp)


router_v1 = routers.DefaultRouter()

router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('users', UserViewSetForAdmin, basename='users')


urlpatterns = [
    path('v1/auth/signup/', APISignUp.as_view(), name='signup'),
    path('v1/auth/token/', APIToken.as_view(), name='token'),
    path('v1/users/me/', APIUser.as_view(), name='me'),
    path('v1/', include(router_v1.urls)),
]
