from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from contents.serializers import AnswerSerializer


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin)