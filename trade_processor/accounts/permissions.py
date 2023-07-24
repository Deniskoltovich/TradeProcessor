from rest_framework import permissions

from accounts.models import Portfolio, User
from recommendations.models import Recommendation


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.USER
        ):
            if isinstance(obj, User):
                return request.user == obj
            elif isinstance(obj, Portfolio):
                return obj.user == request.user
            return obj.portfolio.user == request.user
        return False


class IsAnalyst(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ANALYST
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.USER
        )
