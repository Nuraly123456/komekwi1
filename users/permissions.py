from rest_framework import permissions

class IsAdminUserOnly(permissions.BasePermission):
    """
    Тек рөлі 'admin' болған қолданушыға рұқсат береді
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == 'admin'

