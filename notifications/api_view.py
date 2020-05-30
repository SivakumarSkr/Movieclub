from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwner
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationNewViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsOwner,)
    queryset = Notification.objects.all(unread=True)

    @action(detail=True, methods=['put', 'patch'], url_path='mark_as_read', name='mark_as_read',
            permission_classes=[IsOwner])
    def mark_as_read(self, request, pk=None):
        obj = self.get_object()
        obj.mark_as_read()
        return Response(status=status.HTTP_200_OK)
