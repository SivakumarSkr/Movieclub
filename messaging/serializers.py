from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from messaging.models import Message, Chat
from users.serializers import UserSerializer


class MessageSerializer(ModelSerializer):
    """Model serializer for Message"""

    class Meta:
        model = Message
        fields = ('receiver', 'text', 'image', 'parent')
        read_only_fields = ('uuid_id', 'time', 'sender', 'seen', 'seen_time', 'delivered')


class ChatSerializer(ModelSerializer):
    """ Model serializer for Message"""

    receiver = UserSerializer
    last_active_time = serializers.DateTimeField()
    number_of_unread_message = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ('receiver',)
        read_only_fields = ('uuid_id', 'time_started', 'last_active_time', 'number_of_unread_message')
