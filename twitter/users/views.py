from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from rest_framework import viewsets, permissions, mixins, decorators, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from .permissions import IsUserLoggedIn, IsFollower, IsNotFollower


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsUserLoggedIn()]
        else:
            return []

    @decorators.action(methods=['PUT'], detail=True, permission_classes=[IsNotFollower])
    def follow(self, request, pk):
        # TODO ovo ne bi trebalo followati na obje strane!
        other_user = self.get_object()
        if other_user.followers.filter(pk=request.user.pk).exists():
            return Response(data={'message': 'Already subscribed!'}, status=status.HTTP_200_OK)
        other_user.followers.add(request.user)
        return Response(data={'message': 'Successfully SUBSCRIBED.'}, status=status.HTTP_200_OK)

    @decorators.action(methods=['PUT'], detail=True, permission_classes=[IsFollower])
    def unfollow(self, request, pk):
        other_user = self.get_object()
        if not other_user.followers.filter(pk=request.user.pk).exists():
            return Response(data={'message': 'You are not subscribed to that user!'}, status=status.HTTP_400_BAD_REQUEST)
        other_user.followers.remove(request.user)
        return Response(data={'message': 'Successfully UNSUBSCRIBED!'}, status=status.HTTP_200_OK)
