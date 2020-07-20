from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from contents.models import Blog, Answer, Review, Status


class BlogSerializer(ModelSerializer):
    """Serializer for Blog"""
    like_count = ReadOnlyField(source='like_count')
    dislike_count = ReadOnlyField(source='dislike_count')

    class Meta:
        model = Blog
        fields = ('pk', 'heading', 'contents', 'like_count', 'dislike_count', 'image')
        read_only_fields = ('pk', 'user')


class AnswerSerializer(ModelSerializer):
    """Serializer for Blog"""
    like_count = ReadOnlyField(source='like_count')
    dislike_count = ReadOnlyField(source='dislike_count')

    class Meta:
        model = Answer
        fields = ('pk', 'topic', 'contents', 'like_count', 'dislike_count', 'image')
        readonly_fields = ('pk', 'user')


class ReviewSerializer(ModelSerializer):
    like_count = ReadOnlyField(source='like_count')
    dislike_count = ReadOnlyField(source='dislike_count')

    class Meta:
        model = Review
        fields = ('pk', 'contents', 'image', 'spoiler_alert', 'like_count', 'dislike_count', 'movie')
        readonly_fields = ('pk', 'user')


class StatusSerializer(ModelSerializer):
    like_count = ReadOnlyField(source='like_count')
    dislike_count = ReadOnlyField(source='dislike_count')

    class Meta:
        model = Status
        fields = ('pk', 'time', 'content', 'action', 'like_count', 'dislike_count', 'image')
        read_only_fields = ('pk', 'user', 'time')
