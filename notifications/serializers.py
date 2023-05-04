from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from comments.models import Comment
from comments.serializers import CommentSerializer
from contents.models import Blog, Answer, Review, Status
from contents.serializers import BlogSerializer, AnswerSerializer, ReviewSerializer, StatusSerializer
from groups.models import GroupBlog, Group
from groups.serializers import GroupBlogSerializer, GroupSerializer
from notifications.models import Notification
from shares.models import Share
from shares.serializers import ShareSerializer
from topics.models import Topic
from topics.serializers import TopicSerializer


class NotificationObjectField(Field):
    default_error_messages = {
        'invalid_id': 'Invalid {model_name} object. Please give correct id',
        'invalid_type': "Invalid sharing object type.",
        'invalid_data': "Invalid data. Data should be like '<object-type>/<id of object>'.",
    }

    def to_representation(self, value):
        if isinstance(value, Blog):
            serialize_data = BlogSerializer(value)
        elif isinstance(value, Answer):
            serialize_data = AnswerSerializer(value)
        elif isinstance(value, Review):
            serialize_data = ReviewSerializer(value)
        elif isinstance(value, Share):
            serialize_data = ShareSerializer(value)
        elif isinstance(value, Status):
            serialize_data = StatusSerializer(value)
        elif isinstance(value, GroupBlog):
            serialize_data = GroupBlogSerializer(value)
        elif isinstance(value, Comment):
            serialize_data = CommentSerializer(value)
        elif isinstance(value, Group):
            serialize_data = GroupSerializer(value)
        elif isinstance(value, Topic):
            serialize_data = TopicSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')
        final_data = {'object_type': value.__class__.__name__.lower()}
        final_data.update(serialize_data.data)
        return final_data

    def to_internal_value(self, data):
        object_details = data.split('/')
        if len(object_details) != 2:
            self.fail('invalid_data')
        model_name = object_details[0].lower()
        object_id = object_details[1]
        try:
            if model_name == 'answer':
                shared_object = Answer.objects.get(pk=object_id)
            elif model_name == 'blog':
                shared_object = Blog.objects.get(pk=object_id)
            elif model_name == 'review':
                shared_object = Review.objects.get(pk=object_id)
            elif model_name == 'status':
                shared_object = Status.objects.get(pk=object_id)
            elif model_name == 'share':
                shared_object = Share.objects.get(pk=object_id)
            elif model_name == 'comment':
                shared_object = Comment.objects.get(pk=object_id)
            elif model_name == 'groupblog':
                shared_object = GroupBlog.objects.get(pk=object_id)
            elif model_name == 'group':
                shared_object = Group.objects.get(pk=object_id)
            elif model_name == 'topic':
                shared_object = Group.objects.get(pk=object_id)
            else:
                self.fail("invalid_type")
        except Exception:
            self.fail('invalid_id', model_name=model_name)
        else:
            if shared_object is None:
                self.fail('invalid_id', model_name=model_name)
            return shared_object


class NotificationSerializer(ModelSerializer):
    notification_object = NotificationObjectField(required=True, source='subject_object')

    class Meta:
        model = Notification
        fields = ('creator', 'receiver', 'unread', 'time',
                  'subject_content_type', 'notification_object',)
        read_only_fields = ('creator', 'receiver', 'unread', 'time',
                            'subject_content_type', 'notification_object',)
