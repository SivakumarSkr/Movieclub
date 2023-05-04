from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from contents.serializers import ReviewSerializer, AnswerSerializer, BlogSerializer
from groups.serializers import GroupSerializer
from movies.models import Movie
from movies.serializers import MovieSerializer
from persons.serializers import StarSerializer
from suggestions.serializers import SuggestionSerializer
from topics.serializers import TopicSerializer
from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('email', 'first_name', 'contact_no', 'place')
    authentication_classes = [TokenAuthentication]

    @action(methods=['put'], detail=False, url_path='follow/(?P<pk>[^/.]+)')
    def follow(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['put'], detail=False, url_path='un_follow/(?P<pk>[^/.]+)')
    def un_follow(self, request, pk=None):
        user = User.objects.all()
        user.un_follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=False)
    def get_followers(self, request):
        queryset = request.user.get_followers()
        serialize = UserSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_following(self, request):
        queryset = request.user.get_following()
        serialize = UserSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def followed_topics(self, request):
        queryset = request.user.get_followed_topics()
        serialize = TopicSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def drafted_blog(self, request):
        queryset = request.user.get_drafted_blog()
        serialize = BlogSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def drafted_review(self, request):
        queryset = request.user.get_drafted_review()
        serialize = ReviewSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def drafted_answer(self, request):
        queryset = request.user.get_drafted_answer()
        serialize = AnswerSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def published_blog(self, request):
        queryset = request.user.get_published_blog()
        serialize = BlogSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def published_review(self, request):
        queryset = request.user.get_published_review()
        serialize = ReviewSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def published_answer(self, request):
        queryset = request.user.get_published_answer()
        serialize = AnswerSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def followed_groups(self, request):
        queryset = request.user.get_followed_groups()
        serialize = GroupSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def watched_films(self, request):
        queryset = request.user.get_watched_films()
        serialize = MovieSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def followed_stars(self, request):
        queryset = request.user.get_followed_stars()
        serialize = StarSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def suggestions_received(self, request):
        queryset = request.user.get_suggestions_received()
        serialize = SuggestionSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_suggestions_sent(self, request):
        queryset = request.user.get_suggestions_sent()
        serialize = SuggestionSerializer(queryset)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def check_watched_movie(self, request, pk=None):
        movie = Movie.objects.get(pk=pk)
        check = request.user.check_watched(movie)
        return Response(data=check, status=status.HTTP_100_CONTINUE)

    @action(methods=['patch'], detail=True)
    def activate_prime(self, request, pk=None):
        user = self.get_object()
        status_code = status.HTTP_202_ACCEPTED if user.activate_prime() else status.HTTP_400_BAD_REQUEST
        return Response(status=status_code)


class UserLogin(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
