from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsPrime
from movies.serializers import MovieMiniSerializer
from persons.models import Star
from persons.serializers import StarSerializer


class PersonViewSet(ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'country',)
    permission_classes = (IsAuthenticated, IsPrime)

    # authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, url_path='follow', methods=['patch', 'put'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        person = self.get_object()
        result = person.follow(request.user)
        if result:
            http_status = status.HTTP_202_ACCEPTED
        else:
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(status=http_status)

    @action(detail=True, methods=['patch', 'put'], url_path='un_follow', permission_classes=[IsAuthenticated])
    def un_follow(self, request, pk=None):
        person = self.get_object()
        result = person.un_follow(request.user)
        if result:
            http_status = status.HTTP_202_ACCEPTED
        else:
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(status=http_status)

    @action(detail=True, methods=['get'], url_path='movies_as_director', permission_classes=[IsAuthenticated])
    def get_movies_as_director(self, request, pk=None):
        person = self.get_object()
        movies = person.get_movies_as_director()
        serializer = MovieMiniSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='movies_as_writer', permission_classes=[IsAuthenticated])
    def get_movies_as_writer(self, request, pk=None):
        person = self.get_object()
        movies = person.get_movies_as_writer()
        serializer = MovieMiniSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='movies_as_actor', permission_classes=[IsAuthenticated])
    def get_movies_as_actor(self, request, pk=None):
        person = self.get_object()
        movies = person.get_movies_as_actor()
        serializer = MovieMiniSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
