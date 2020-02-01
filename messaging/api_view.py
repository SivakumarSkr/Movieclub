from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from messaging.models import Message, Chat
from messaging.permissions import IsOwner, IsReceiver, IsChatParticipate
from messaging.serializers import MessageSerializer, ChatSerializer


class MessageVewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsOwner, IsReceiver]
    authentication_classes = [TokenAuthentication]
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(methods=['patch'], detail=True, permission_classes=[IsReceiver])
    def set_seen(self, request, pk=None):
        message = Message.objects.get(pk=pk)
        message.set_seen()
        return Response(status=status.HTTP_202_ACCEPTED)


class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsChatParticipate]
    authentication_classes = [TokenAuthentication]
    queryset = Chat.objects.all()

    def perform_create(self, serializer):
        pass
