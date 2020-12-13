from rest_framework import permissions


class EditBookPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(
                name="Provider") or request.user.groups.filter(name="Support")

        return False

    def has_object_permission(self, request, view, obj):
        return True


class DeleteBookPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name="Support")

        return False

    def has_object_permission(self, request, view, obj):
        return True
