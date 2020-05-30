from rest_framework.serializers import ModelSerializer

from notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ('creator', 'receiver', 'unread', 'time', 'category',
                  'subject_content_type', 'subject_object',)
        read_only_fields = ('creator', 'receiver', 'unread', 'time', 'category',
                            'subject_content_type', 'subject_object',)
