from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from twitter.tweets.views import TweetViewSet, TagViewSet
from twitter.users.views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(r'web-auth/', include('rest_framework.urls')),
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'api/', include(router.urls)),
]
