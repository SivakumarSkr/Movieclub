from rest_framework.serializers import ModelSerializer

from contents.models import Blog, Answer, Review, Status


class BlogSerializer(ModelSerializer):
    """Serializer for Blog"""
    class Meta:
        model = Blog
        fields = ('tags', 'contents', 'image', 'heading')


class AnswerSerializer(ModelSerializer):
    """Serializer for Blog"""

    class Meta:
        model = Answer
        fields = ('tags', 'contents', 'image')


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ('tags', 'contents', 'image', 'spoiler_alert')


class StatusSerializer(ModelSerializer):

    class Meta:
        model = Status
        fields = ('content', 'action', 'image')
