from rest_framework.serializers import ModelSerializer

from persons.models import Star


class StarSerializer(ModelSerializer):
    # followers_count = ReadOnlyField()

    class Meta:
        model = Star
        fields = (
            'pk', 'name', 'date_of_birth', 'country', 'photo', 'biography', 'followers', 'followers_count',
            'created_by', 'updated_by', 'number_of_films_as_director', 'number_of_films_as_actor',
            'number_of_films_as_writer'
        )
        read_only_fields = ('pk', 'followers', 'created_by', 'updated_by', 'number_of_films_as_director',
                            'number_of_films_as_actor', 'number_of_films_as_writer'
                            )

    def update(self, instance, validated_data):
        user = None
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            user = request.user
        instance.updated_by = user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StarMiniSerializer(ModelSerializer):
    class Meta:
        model = Star
        fields = ('pk', 'name')
        read_only_fields = ('name',)
