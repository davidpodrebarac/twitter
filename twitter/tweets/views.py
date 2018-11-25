from rest_framework import viewsets, permissions

from twitter.tweets import extract_tags_from_description
from .models import Tweet, Tag, create_tag_objects_from_tags
from .permissions import IsTweetOwner
from .serializers import TweetSerializer, TagSerializer


class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = TweetSerializer

    def get_queryset(self):
        queryset = Tweet.objects
        if 'subscribed' in self.request.query_params:
            try:
                if bool(self.request.query_params['subscribed']):
                    queryset = queryset.filter(creator__in=self.request.user.follows.all())
            except:
                pass
        return queryset.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsTweetOwner()]
        else:  # create
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        tags = extract_tags_from_description(serializer.validated_data['text'])
        tag_list = create_tag_objects_from_tags(tags)
        serializer.save(creator=self.request.user, tags=tag_list)

    def perform_update(self, serializer):
        tags = extract_tags_from_description(serializer.validated_data['text'])
        tag_list = create_tag_objects_from_tags(tags)
        serializer.save(tags=tag_list)


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
