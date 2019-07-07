from rest_framework import permissions


class AdminPermissions(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        return bool(request.user and request.user.is_authenticated and (request.user.role.level is 0))
