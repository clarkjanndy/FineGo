from rest_framework.permissions import BasePermission, SAFE_METHODS

__all__ = ['NotAuthenticated', 'IsAdminOrReadOnly']

class NotAuthenticated(BasePermission, ):
    def has_permission(self, request, view):
        return not request.user.is_authenticated    

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        # Check if the user is an admin
        return request.user.is_authenticated and request.user.is_superuser


