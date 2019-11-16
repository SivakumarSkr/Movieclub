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
        fields = ('topic', 'contents', 'image')


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ('contents', 'image', 'spoiler_alert', 'movie')


class StatusSerializer(ModelSerializer):

    class Meta:
        model = Status
        fields = ('content', 'action', 'image')
