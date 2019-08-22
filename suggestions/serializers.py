from rest_framework.serializers import ModelSerializer

from suggestions.models import Suggestion


class SuggestionSerializer(ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ('sender', 'receiver', 'time', 'content_type', 'content_object')
        read_only_fields = ('sender', 'receiver', 'time',)
