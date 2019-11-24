from rest_framework.serializers import ModelSerializer

from topics.models import Topic


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ('head', 'time', 'description', 'created_by', 'no_of_watches',
                  )
        read_only_fields = ('time', 'created_by', 'no_of_watches')
