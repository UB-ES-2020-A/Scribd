from rest_framework import permissions

class CustomPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Providers').exists() or \
               request.user.groups.filter(name='Supports').exists() or \
               request.user.groups.filter(name='Admin').exists()

    def has_object_permission(self, request, view, obj):
        return True