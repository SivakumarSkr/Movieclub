from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from topics.models import Topic


class TopicSerializer(ModelSerializer):
    followers_count = ReadOnlyField()

    class Meta:
        model = Topic
        fields = ('pk', 'head', 'time', 'description', 'answer_count', 'created_by', 'no_of_watches', 'followers_count')
        read_only_fields = ('pk', 'time', 'created_by', 'answer_count', 'no_of_watches')
