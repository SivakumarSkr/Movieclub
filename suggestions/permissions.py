from rest_framework.permissions import BasePermission


class SuggestionPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.user == obj.sender) or (request.user == obj.receiver):
            return True
