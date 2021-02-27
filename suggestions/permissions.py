from rest_framework.permissions import BasePermission, SAFE_METHODS


class SuggestionPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.user == obj.sender) or (request.user == obj.receiver):
            return True


class SenderPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.sender == request.user or obj.receiver == request.user
        return obj.sender == request.user


class ReceiverPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.sender == request.user or obj.receiver == request.user
        return obj.receiver == request.user
