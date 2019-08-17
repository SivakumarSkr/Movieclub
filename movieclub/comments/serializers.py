
from rest_framework.serializers import ModelSerializer

from comments.models import Comment


class CommentSerializer(ModelSerializer):

    """Model serializer for Comment"""
    class Meta:
        model = Comment
        fields = ('text',)
