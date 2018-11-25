from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from twitter.tweets.views import TweetViewSet, TagViewSet
from twitter.users.views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name='user')
router.register(r'tweets', TweetViewSet, base_name='tweets')
router.register(r'tags', TagViewSet, base_name='tags')

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(r'web-auth/', include('rest_framework.urls')),
    path(r'api-token-auth/', obtain_jwt_token, name='login'),
    path(r'api/', include(router.urls)),
]
