from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwner, IsPrime
from movies.models import Movie, Language, Genre, Rating
from movies.serializers import MovieSerializer, LanguageSerializer, GenreSerializer, RatingSerializer


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated, IsPrime)
    # authentication_classes = [TokenAuthentication]
    queryset = Movie.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    permission_classes = (IsPrime,)
    # authentication_classes = [TokenAuthentication]
    queryset = Language.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['put'], url_path='follow', name='follow_language',
            permission_classes=[IsAuthenticated])
    def follow_language(self, request, pk=None):
        language = self.get_object()
        language.follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED, data='Now you are following {}.'.format(request.user))

    @action(detail=True, methods=['put'], url_path='un_follow', name='un_follow_language',
            permission_classes=[IsAuthenticated])
    def un_follow_language(self, request, pk=None):
        language = self.get_object()
        language.un_follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated, IsPrime)
    # authentication_classes = [TokenAuthentication]
    queryset = Genre.objects.all()
    search_fields = ('name', 'released_year', 'country', 'director__name', 'language__name', 'stars__name')

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['put'], url_path='follow', name='follow_genre', permission_classes=[IsAuthenticated])
    def follow_genre(self, request, pk=None):
        genre = self.get_object()
        genre.follow(request.user)
        return Response(data='Now you following {}.'.format(self.name), status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['put'], url_path='un_follow', name='un_follow_genre',
            permission_classes=[IsAuthenticated])
    def un_follow_genre(self, request, pk=None):
        genre = self.get_object()
        genre.un_follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = (IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        movie_id = self.request.POST.get('movie', None)
        movie = Movie.objects.get(pk=movie_id)
        serializer.save(created_by=self.request.user, movie=movie)
