from rest_framework import permissions


class EditBookPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Admin').exists() or \
               request.user.groups.filter(name='Support').exists() or \
               request.user.groups.filter(name='Provider').exists()

    def has_object_permission(self, request, view, obj):
        return True


class DeleteBookPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Admin').exists() or \
               request.user.groups.filter(name='Support').exists()

    def has_object_permission(self, request, view, obj):
        return True
