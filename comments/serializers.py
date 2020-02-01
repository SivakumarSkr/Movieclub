from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from comments.models import Comment
from contents.models import Blog, Answer, Review, Status


class CommentSerializer(ModelSerializer):
    """Model serializer for Comment"""
    comment_object = GenericRelatedField({
        Blog: serializers.HyperlinkedRelatedField(
            queryset=Blog.objects.all(),
            view_name='blog-detail',
        ),
        Answer: serializers.HyperlinkedRelatedField(
            queryset=Answer.objects.all(),
            view_name='answer-detail',
        ),
        Review: serializers.HyperlinkedRelatedField(
            queryset=Review.objects.all(),
            view_name='review-detail',
        ),
        Comment: serializers.HyperlinkedRelatedField(
            queryset=Comment.objects.all(),
            view_name='comment-detail',
        ),
        Status: serializers.HyperlinkedRelatedField(
            queryset=Status.objects.all(),
            view_name='status-detail',
        ),

    })

    class Meta:
        model = Comment
        fields = ('uuid_id', 'user', 'time', 'text', 'image', 'comment_object')
        read_only_fields = ('uuid_id', 'user', 'time')
