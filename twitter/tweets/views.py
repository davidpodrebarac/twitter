from rest_framework import viewsets, permissions
from .models import Tweet, Tag
from .serializers import TweetSerializer, TagSerializer
from .permissions import IsTweetOwner


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly()]  # even unregistreted users can see tweets
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTweetOwner()]
        else:  # create
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action in ['create']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]
