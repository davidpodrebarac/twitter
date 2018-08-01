from rest_framework import permissions


class IsUserLoggedIn(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsFollower(permissions.BasePermission):
    """
    Custom permission to only allow followers to unsubsribe
    """

    def has_object_permission(self, request, view, obj):
        return obj.followers.filter(pk=request.user.pk).exists()


class IsNotFollower(IsFollower):

    def has_object_permission(self, request, view, obj):
        return not super().has_object_permission(request, view, obj)
