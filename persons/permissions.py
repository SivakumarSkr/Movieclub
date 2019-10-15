from rest_framework.permissions import BasePermission


class StarPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        pass