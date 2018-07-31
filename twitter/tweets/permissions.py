from rest_framework import permissions


class IsTweetOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a tweet to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
