from rest_framework import viewsets, permissions, decorators
from rest_framework.response import Response

from .models import Tweet, Tag
from .serializers import TweetSerializer, TagSerializer
from .permissions import IsTweetOwner
from rest_framework.generics import ListAPIView


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly()]  # even unregistreted users can see tweets
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsTweetOwner()]
        else:  # create
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @decorators.action(methods=['GET'], detail=False, permission_classes=[permissions.IsAuthenticated],
                       url_path='private-timeline')
    def private_timeline(self, request, pk=None):
        queryset = Tweet.objects.filter(creator__in=self.request.user.follows.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
