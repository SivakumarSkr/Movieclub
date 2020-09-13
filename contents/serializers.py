from rest_framework.serializers import ModelSerializer

from contents.models import Blog, Answer, Review, Status


class BlogSerializer(ModelSerializer):
    """Serializer for Blog"""
    class Meta:
        model = Blog
        fields = ('pk', 'heading', 'contents', 'status', 'like_count', 'dislike_count', 'image')
        read_only_fields = ('pk', 'user', 'like_count', 'dislike_count')


class AnswerSerializer(ModelSerializer):
    """Serializer for Blog"""

    class Meta:
        model = Answer
        fields = ('pk', 'topic', 'contents', 'status', 'like_count', 'dislike_count', 'image')
        readonly_fields = ('pk', 'user', 'like_count', 'like_count', 'status')


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ('pk', 'contents', 'image', 'status', 'spoiler_alert', 'like_count', 'dislike_count', 'movie')
        readonly_fields = ('pk', 'user', 'like_count', 'like_count')


class StatusSerializer(ModelSerializer):

    class Meta:
        model = Status
        fields = ('pk', 'time', 'content', 'action', 'like_count', 'dislike_count', 'image')
        read_only_fields = ('pk', 'user', 'time', 'like_count', 'like_count')
