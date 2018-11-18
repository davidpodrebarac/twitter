from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from twitter.users.views import UserViewSet
from twitter.tweets.views import TweetViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "users/",
        include("twitter.users.urls", namespace="users"),
    ),
    url(r'^api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^api-token-auth/', obtain_jwt_token),
    # Your stuff: custom urls includes go here
    path('api/', include(router.urls)),
]
