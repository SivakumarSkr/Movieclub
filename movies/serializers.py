from rest_framework.serializers import ModelSerializer

from movies.models import Genre, Language, Movie, Rating


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('pk', 'name', 'thumbnail')
        read_only_fields = ('pk', 'followers',)


class LanguageSerializer(ModelSerializer):

    class Meta:
        model = Language
        fields = ('pk', 'name', 'thumbnail')
        read_only_fields = ('pk', 'followers')


class MovieSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = ('pk', 'name', 'released_year', 'language', 'genre', 'country',
                  'director', 'writers', 'stars', 'thumbnail',)
        read_only_fields = ('pk', 'rating',)


class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = ('pk', 'movie', 'user', 'rate')
        read_only_fields = ('pk',)
