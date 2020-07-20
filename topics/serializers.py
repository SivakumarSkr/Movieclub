from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from topics.models import Topic


class TopicSerializer(ModelSerializer):
    followers_count = ReadOnlyField(source='followers_count')

    class Meta:
        model = Topic
        fields = ('head', 'time', 'description', 'created_by', 'no_of_watches', 'followers_count')
        read_only_fields = ('time', 'created_by', 'no_of_watches')
