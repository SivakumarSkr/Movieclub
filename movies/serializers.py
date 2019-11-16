from rest_framework.serializers import ModelSerializer

from movies.models import Genre, Language, Movie, Rating


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'thumbnail')


class LanguageSerializer(ModelSerializer):

    class Meta:
        model = Language
        fields = ('name', 'thumbnail')


class MovieSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = ('name', 'released_year', 'language', 'genre', 'country',
                  'director', 'rating', 'writers', 'stars', 'thumbnail',)


class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = ('movie', 'user', 'rate')
