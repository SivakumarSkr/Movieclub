from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from suggestions.serializers import SuggestionSerializer
from topics.permissions import TopicPermission


class SuggestionViewSet(ModelViewSet):
    serializer_class = SuggestionSerializer
    permission_classes = (IsAuthenticated, TopicPermission,)
    # authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        received = self.request.user.get_suggestions_received()
        sent = self.request.user.get_suggestions_sent()
        return received | sent
