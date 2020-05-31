from generic_relations.relations import GenericRelatedField
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import ModelSerializer

from contents.models import Blog, Answer, Review
from shares.models import Share


class ShareSerializer(ModelSerializer):
    shared_object = GenericRelatedField({
        Blog: HyperlinkedRelatedField(
            queryset=Blog.objects.all(),
            view_name='blog-detail',
        ),
        Answer: HyperlinkedRelatedField(
            queryset=Answer.objects.all(),
            view_name='answer-detail',
        ),
        Review: HyperlinkedRelatedField(
            queryset=Review.objects.all(),
            view_name='review-detail',
        ),
    }, source='sharing_object')

    class Meta:
        model = Share
        fields = ('pk', 'time', 'user', 'liked', 'shared_object', 'description', 'set_comments')
        read_only_fields = ('pk', 'time', 'user', 'liked', 'set_comments')
