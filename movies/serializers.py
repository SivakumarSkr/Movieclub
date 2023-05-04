from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from movies.models import Genre, Language, Movie, Rating


class GenreSerializer(ModelSerializer):
    followers_count = ReadOnlyField()

    class Meta:
        model = Genre
        fields = ('pk', 'name', 'thumbnail', 'followers_count')
        read_only_fields = ('pk', 'followers',)


class LanguageSerializer(ModelSerializer):
    followers_count = ReadOnlyField()

    class Meta:
        model = Language
        fields = ('pk', 'name', 'thumbnail', 'followers_count')
        read_only_fields = ('pk', 'followers')


class MovieSerializer(ModelSerializer):
    rating_count = ReadOnlyField(source='number_of_rates')

    # writers = StarMiniSerializer(read_only=True, many=True)
    # directors = StarMiniSerializer(read_only=True, many=True)
    # stars = StarMiniSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('pk', 'name', 'released_year', 'rating', 'language', 'genre', 'country',
                  'directors', 'writers', 'stars', 'thumbnail', 'rating_count')
        read_only_fields = ('pk', 'rating',)


class MovieMiniSerializer(MovieSerializer):
    class Meta:
        model = Movie
        fields = ('pk', 'name')
        read_only_fields = ('pk', 'name')


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('pk', 'movie', 'user', 'rate')
        read_only_fields = ('pk', 'user')
