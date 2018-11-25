from rest_framework import viewsets, permissions, mixins, decorators, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twitter.tweets.models import Tweet
from twitter.tweets.serializers import TweetSerializer
from .models import User
from .permissions import IsOwnerLoggedIn
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    """
        URL::

            /api/users

        GET - returns a list of all users in app, pagination supported:

            Response 200::

                {
                    "count": int,
                    "next": str,
                    "previous": str,
                    "results": [
                        {
                            "id": int,
                            "username": str,
                            "full_name": str,
                            "email": str,
                            "is_active": bool,
                            "date_joined": datetime,
                            "followers": [hyperlink, ...],
                            "follows": [hyperlink, ...],
                        },
                    ]
                }

        URL::

            /api/users/<pk>

        GET - return detail information about user with matching pk:

            Response 200::

                {
                    "id": int,
                    "username": str,
                    "full_name": str,
                    "email": str,
                    "is_active": bool,
                    "date_joined": datetime,
                    "followers": [hyperlink, ...],
                    "follows": [hyperlink, ...],
                }

        PUT - update user info:
            User can only edit his own profile! Attributes that be editer are: username, full_name, email.

            Request::

                {
                    "username": str,
                    "full_name": str,
                    "email": str,
                }

            Response 200::

                {
                    "id": int,
                    "username": str,
                    "full_name": str,
                    "email": str,
                    "is_active": bool,
                    "date_joined": datetime,
                    "followers": [hyperlink, ...],
                    "follows": [hyperlink, ...],
                }

        DELETE - delete user with matching pk:
            Only tweet owner can delete his account.

            Response 204::

                {}

        URL::

            /api/users/<pk>/(un)follow

        PUT - currently logined user starts following user with given pk:

            Response 200::

                {
                    "message": str,
                }

        URL::

            /api/users/<pk>/tweets

        GET - list tweets created by user with matching `pk`:

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

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerLoggedIn()]
        else:
            return [permissions.IsAuthenticated()]

    @decorators.action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        other_user = self.get_object()
        if other_user.followers.filter(pk=request.user.pk).exists():
            return Response(data={'message': 'Already SUBSCRIBED!'}, status=status.HTTP_200_OK)
        other_user.followers.add(request.user)
        return Response(data={'message': 'Successfully subscribed.'}, status=status.HTTP_200_OK)

    @decorators.action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        other_user = self.get_object()
        if not other_user.followers.filter(pk=request.user.pk).exists():
            return Response(data={'message': 'Already UNSUBSCRIBED'}, status=status.HTTP_400_BAD_REQUEST)
        other_user.followers.remove(request.user)
        return Response(data={'message': 'Successfully unsubscribed!'}, status=status.HTTP_200_OK)

    @decorators.action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def tweets(self, request, pk):
        user_tweets = Tweet.objects.filter(creator_id=pk).all()
        return Response(data=TweetSerializer(user_tweets, many=True, context={'request': request}).data)
