from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwner, IsPrime
from movies.models import Movie, Language, Genre, Rating
from movies.serializers import MovieSerializer, LanguageSerializer, GenreSerializer, RatingSerializer


class MoviePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BaseViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsPrime)

    @action(detail=True, methods=['put'], url_path='follow', name='follow',
            permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        obj = self.get_object()
        obj.follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['put'], url_path='un_follow', name='un_follow',
            permission_classes=[IsAuthenticated])
    def un_follow(self, request, pk=None):
        obj = self.get_object()
        obj.un_follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class MovieViewSet(BaseViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = MoviePagination

    def perform_create(self, serializer):
        serializer.save()


class LanguageViewSet(BaseViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(BaseViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    search_fields = ('name', 'released_year', 'country', 'director__name', 'language__name', 'stars__name')

    def perform_create(self, serializer):
        serializer.save()


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
