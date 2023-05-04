from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comments.api_view import CommentPagination
from comments.serializers import CommentSerializer
from contents.models import Answer, Blog, Review, Status
from contents.permissions import IsOwner
from contents.serializers import AnswerSerializer, BlogSerializer, ReviewSerializer, StatusSerializer
from users.serializers import UserSerializer

User = get_user_model()


class CommonLikesPaginator(PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'page-size'
    max_page_size = 1000


class ContentPaginator(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page-size'
    max_page_size = 1000


class ContentViewSet(ModelViewSet):
    pagination_class = ContentPaginator

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['patch'], detail=True, url_path='like', permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        content = self.get_object()
        content.like(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='dislike', permission_classes=[IsAuthenticatedOrReadOnly])
    def dislike(self, request, pk=None):
        content = self.get_object()
        content.dislike(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get_comments', permission_classes=[IsAuthenticatedOrReadOnly],
            pagination_class=CommentPagination)
    def get_comments(self, request, pk=None):
        content = self.get_object()
        comments = content.get_comments()
        serialize = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='common_likes', permission_classes=[IsAuthenticatedOrReadOnly],
            pagination_class=CommonLikesPaginator)
    def get_common_liked_user(self, request, pk=None):
        content = self.get_object()
        common_likes = content.get_common_likes(request.user)
        serialize = UserSerializer(common_likes, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['put', 'patch'], detail=True, url_path='save_draft', permission_classes=[IsOwner])
    def save_draft(self, request, pk=None):
        content = self.get_object()
        serializer = self.serializer_class(content, data=request.data)
        if serializer.is_valid() and content.status != 'P':
            serializer.save(status='D', user=request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'patch'], detail=True, url_path='publish', permission_classes=[IsOwner])
    def publish(self, request, pk=None):
        content = self.get_object()
        serializer = self.serializer_class(content, data=request.data)
        if serializer.is_valid():
            serializer.save(status='P', user=request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Answer.objects.all()


class BlogViewSet(ContentViewSet):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Blog.objects.all()


class ReviewViewSet(ContentViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()


class StatusVewSet(ContentViewSet):
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Status.objects.all()
