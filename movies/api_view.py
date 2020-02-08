from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from movies.models import Movie, Language, Genre, Rating
from movies.permissions import Permission, IsOwner
from movies.serializers import MovieSerializer, LanguageSerializer, GenreSerializer, RatingSerializer


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = (Permission,)
    authentication_classes = [TokenAuthentication]
    queryset = Movie.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    permission_classes = (Permission,)
    # authentication_classes = [TokenAuthentication]
    queryset = Language.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['put'], url_path='follow/(?P<pk>[^/.]+)', name='follow_language')
    def follow_language(self, request, pk=None):
        language = self.get_object()
        language.follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED, data='Now you are following {}.'.format(request.user))


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (Permission,)
    # authentication_classes = [TokenAuthentication]
    queryset = Genre.objects.all()
    search_fields = ('name', 'released_year', 'country', 'director__name', 'language__name', 'stars__name')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['put'], url_path='follow/(?P<pk>[^/.]+)', name='follow_genre')
    def follow_genre(self, request, pk=None):
        genre = self.get_object()
        genre.follow(request.user)
        return Response(data='Now you following {}.'.format(self.name), status=status.HTTP_202_ACCEPTED)


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = (IsOwner, IsAuthenticated)
    authentication_classes = [TokenAuthentication]
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



