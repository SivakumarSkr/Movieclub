from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from contents.models import Answer, Blog, Review
from contents.serializers import BlogSerializer, AnswerSerializer, ReviewSerializer
from movies.models import Movie
from movies.serializers import MovieSerializer
from suggestions.models import Suggestion
from topics.models import Topic
from topics.serializers import TopicSerializer


class SuggestionObjectField(Field):
    default_error_messages = {
        'invalid_id': 'Invalid {model_name} object. Please give correct id',
        'invalid_type': "Invalid sharing object type.",
        'invalid_data': "Invalid data. Data should be like '<object-type>/<id of object>'.",
    }

    def to_representation(self, value):
        if isinstance(value, Blog):
            serialize_data = BlogSerializer(value)
        elif isinstance(value, Answer):
            serialize_data = AnswerSerializer(value)
        elif isinstance(value, Review):
            serialize_data = ReviewSerializer(value)
        elif isinstance(value, Movie):
            serialize_data = MovieSerializer(value)
        elif isinstance(value, Topic):
            serialize_data = TopicSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')
        final_data = {'object_type': value.__class__.__name__.lower()}
        final_data.update(serialize_data.data)
        return final_data

    def to_internal_value(self, data):
        object_details = data.split('/')
        if len(object_details) != 2:
            self.fail('invalid_data')
        model_name = object_details[0].lower()
        object_id = object_details[1]
        try:
            if model_name == 'answer':
                shared_object = Answer.objects.get(pk=object_id)
            elif model_name == 'blog':
                shared_object = Blog.objects.get(pk=object_id)
            elif model_name == 'review':
                shared_object = Review.objects.get(pk=object_id)
            elif model_name == 'movie':
                shared_object = Movie.objects.get(pk=object_id)
            elif model_name == 'topic':
                shared_object = Topic.objects.get(pk=object_id)
            else:
                self.fail("invalid_type")
        except Exception:
            self.fail('invalid_id', model_name=model_name)
        else:
            if shared_object is None:
                self.fail('invalid_id', model_name=model_name)
            return shared_object


class SuggestionSerializer(ModelSerializer):
    suggesting_object = SuggestionObjectField(required=True, source='content_object')

    class Meta:
        model = Suggestion
        fields = ('pk', 'sender', 'receiver', 'time', 'response', 'suggesting_object')
        read_only_fields = ('pk', 'sender', 'receiver', 'time', 'response')
