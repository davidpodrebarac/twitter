from rest_framework import viewsets, permissions, generics

from twitter.tweets import extract_tags_from_description
from .models import Tweet, Tag, create_tag_objects_from_tags
from .permissions import IsTweetOwner
from .serializers import TweetSerializer, TagSerializer


class TweetViewSet(viewsets.ModelViewSet):
    """
        URL::

            /api/tweets

        GET - returns all tweets(public timeline) or private tweets(private timeline, only subscribed users), pagination supported:
            Queryparam subscribed is not mandatory, but if it is sent and is equal to True then server returns only tweets from
            subscribed users.

            Request::

                {
                    "subscribed": bool,
                }

            Response 200::

                {
                    "count": int,
                    "next": str,
                    "previous": str,
                    "results": [
                        {
                            "id": int,
                            "text": str,
                            "created": datetime-str,
                            "creator": user-link,
                            "tags": [
                                {
                                    "id": id,
                                    "name": str,
                                }, ..
                            ]
                        }, ...
                    ]
                }

        POST - create new tweet:
            Tags(strings starting with #) are not required; they are parsed from text.

            Request::

                {
                    "text": str,
                }

            Response 201::

                {
                    "id": int,
                    "text": str,
                    "created": datetime-str,
                    "creator": user-link,
                    "tags": [
                        {
                            "id": id,
                            "name": str,
                        }, ..
                    ]
                }

        URL::

            /api/tweets/<pk>

        GET - return detail information about tweet with matching id:

            Response 200::

                {
                    "id": int,
                    "text": str,
                    "created": datetime-str,
                    "creator": user-link,
                    "tags": [
                        {
                            "id": id,
                            "name": str,
                        }, ..
                    ]
                }

        PUT - update existing tweet with matching pk:
            Only text can be updated.

            Request::

                {
                    "text": str,
                }

            Response 200::

                {
                    "id": int,
                    "text": str,
                    "created": datetime-str,
                    "creator": user-link,
                    "tags": [
                        {
                            "id": id,
                            "name": str,
                        }, ..
                    ]
                }

        DELETE - delete tweet with matching pk:
            Only tweet owner can delete tweet.

            Response 204::

                {}

    """
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


class TagViewSet(viewsets.GenericViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
