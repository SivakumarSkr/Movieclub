from rest_framework.serializers import ModelSerializer

from contents.models import Blog, Answer, Review, Status


class BlogSerializer(ModelSerializer):
    """Serializer for Blog"""
    class Meta:
        model = Blog
        fields = ('heading', 'contents', 'image')


class AnswerSerializer(ModelSerializer):
    """Serializer for Blog"""

    class Meta:
        model = Answer
        fields = ('pk', 'topic', 'contents', 'image')
        readonly_fields = ('pk', 'user')


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ('pk', 'contents', 'image', 'spoiler_alert', 'movie')
        readonly_fields = ('pk', 'user')


class StatusSerializer(ModelSerializer):

    class Meta:
        model = Status
        fields = ('pk', 'content', 'action', 'image')
        readonly_fields = ('pk', 'user')