from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Moderator').exists()

class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.groups.filter(name='Moderator').exists()

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsModeratorOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Moderator').exists():
            return True
        return obj.owner == request.user