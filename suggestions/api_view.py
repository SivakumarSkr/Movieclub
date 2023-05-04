from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from suggestions.permissions import ReceiverPermission, SenderPermission
from suggestions.serializers import SuggestionSerializer, SuggestionRespond


class SuggestionViewSet(ModelViewSet):
    serializer_class = SuggestionSerializer
    permission_classes = (IsAuthenticated, SenderPermission,)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        received = self.request.user.get_suggestions_received()
        sent = self.request.user.get_suggestions_sent()
        return received | sent

    @action(detail=True, methods=['put', 'patch'], url_path='accept', permission_classes=[ReceiverPermission])
    def accept_suggestion(self, request, pk=None):
        suggestion = self.get_object()
        status_of_accepted = status.HTTP_200_OK if suggestion.accept() else status.HTTP_400_BAD_REQUEST
        return Response(status=status_of_accepted)

    @action(detail=True, methods=['put', 'patch'], url_path='respond', serializer_class=SuggestionRespond,
            permission_classes=[IsAuthenticated, ReceiverPermission])
    def respond(self, request, pk=None):
        suggestion = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            suggestion.respond(serializer.data.get('response'))
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
