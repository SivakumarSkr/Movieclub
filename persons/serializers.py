from rest_framework.serializers import ModelSerializer

from persons.models import Star


class StarSerializer(ModelSerializer):
    class Meta:
        model = Star
        fields = ('name', 'date_of_birth', 'country', 'photo', 'biography', 'followers')
        # read_only_fields = ('followers', )
