from rest_framework import permissions

from accounts.models import Portfolio, User


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == request.user.Role.ADMIN
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.user
            and request.user.is_authenticated
            and request.user.role == request.user.Role.USER
        ):
            if type(obj) == User:
                return request.user == obj
            elif type(obj) in (Portfolio,):
                return obj.user == request.user
            return obj.portfolio.user == request.user
        return False


class IsAnalyst(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == request.user.Role.ANALYST
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == request.user.Role.USER
        )
