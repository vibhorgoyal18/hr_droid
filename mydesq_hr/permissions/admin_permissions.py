from rest_framework import permissions
from users.models import UserDetails


class AdminPermissions(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        user_details = UserDetails.objects.get(user=request.user)
        return bool(request.user and request.user.is_authenticated and (user_details.role_id is 1))
