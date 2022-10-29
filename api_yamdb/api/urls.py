from django.urls import include, path
from rest_framework import routers

from api.views import (GenreViewSet, CategoryViewSet,
                       UserViewSet, AuthClass)


router_v1 = routers.DefaultRouter()

router_v1.register('auth', AuthClass, basename='auth_users')
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
