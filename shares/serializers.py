from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from contents.models import Blog, Answer, Review
from contents.serializers import BlogSerializer, AnswerSerializer, ReviewSerializer
from shares.models import Share


class SharedObjectField(Field):
    default_error_messages = {
        'invalid_id': 'Invalid {model_name} object. Please give correct id',
        'invalid_type': "Invalid sharing object type.",
        'invalid_data': "Invalid Data. data should be like '<object-type>/<id of object>'.",
    }

    def to_representation(self, value):
        if isinstance(value, Blog):
            serialize_data = BlogSerializer(value)
        elif isinstance(value, Answer):
            serialize_data = AnswerSerializer(value)
        elif isinstance(value, Review):
            serialize_data = ReviewSerializer(value)
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
            else:
                self.fail("invalid_type")
        except Exception:
            self.fail('invalid_id', model_name=model_name)
        else:
            if shared_object is None:
                self.fail('invalid_id', model_name=model_name)
            return shared_object


class ShareSerializer(ModelSerializer):
    sharing_object = SharedObjectField(required=True, source='sharing_object')

    class Meta:
        model = Share
        fields = ('pk', 'time', 'user', 'liked', 'sharing_object', 'description')
        read_only_fields = ('pk', 'time', 'user', 'liked')
