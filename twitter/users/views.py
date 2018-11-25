from rest_framework import viewsets, permissions, mixins, decorators, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import IsOwnerLoggedIn, IsFollower, IsNotFollower
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerLoggedIn()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

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
