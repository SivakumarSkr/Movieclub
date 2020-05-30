from rest_framework.serializers import ModelSerializer

from movies.models import Genre, Language, Movie, Rating


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'thumbnail')
        read_only_fields = ('followers',)


class LanguageSerializer(ModelSerializer):

    class Meta:
        model = Language
        fields = ('pk', 'name', 'thumbnail')
        read_only_fields = ('pk', 'followers')


class MovieSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = ('name', 'released_year', 'language', 'genre', 'country',
                  'director', 'writers', 'stars', 'thumbnail',)
        read_only_fields = ('rating',)


class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = ('movie', 'user', 'rate')
