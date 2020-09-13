from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from movies.models import Genre, Language, Movie, Rating


class GenreSerializer(ModelSerializer):
    followers_count = ReadOnlyField(source='followers_count')

    class Meta:
        model = Genre
        fields = ('uuid_id', 'name', 'thumbnail', 'followers_count')
        read_only_fields = ('uuid_id', 'followers',)


class LanguageSerializer(ModelSerializer):
    followers_count = ReadOnlyField(source='followers_count')

    class Meta:
        model = Language
        fields = ('uuid_id', 'name', 'thumbnail', 'followers_count')
        read_only_fields = ('uuid_id', 'followers')


class MovieSerializer(ModelSerializer):
    rating_count = ReadOnlyField(source='number_of_rates')

    class Meta:
        model = Movie
        fields = ('uuid_id', 'name', 'released_year', 'language', 'genre', 'country',
                  'director', 'writers', 'stars', 'thumbnail', 'rating_count')
        read_only_fields = ('uuid_id', 'rating',)


class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = ('uuid_id', 'movie', 'user', 'rate')
        read_only_fields = ('uuid_id',)
