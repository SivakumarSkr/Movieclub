from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comments.serializers import CommentSerializer
from contents.models import Answer, Blog, Review, Status
from contents.permissions import IsOwner
from contents.serializers import AnswerSerializer, BlogSerializer, ReviewSerializer, StatusSerializer
from users.serializers import UserSerializer

User = get_user_model()


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['patch'], detail=True, url_path='like', permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        answer = Answer.objects.get(pk=pk)
        answer.like_the_content(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='dislike', permission_classes=[IsAuthenticatedOrReadOnly])
    def un_like(self, request, pk=None):
        answer = Answer.objects.get(pk=pk)
        answer.dislike_the_content(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_likes(self, request, pk=None):
        answer = Answer.objects.get(pk=pk)
        likes = answer.get_likes()
        return Response(data={'likes': likes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-dislikes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_dislikes(self, request, pk=None):
        answer = Answer.objects.get(pk=pk)
        dislikes = answer.get_dislike()
        return Response(data={'dislikes': dislikes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-comments', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_comments(self, request, pk=None):
        answer = Answer.objects.get(pk=pk)
        comments = answer.get_comments()
        serialize = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='common-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_common_liked_user(self, request, pk=None):
        answer = Blog.objects.get(pk=pk)
        common_likes = answer.get_common_likes(request.user)
        serialize = UserSerializer(common_likes, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['patch'], detail=True, url_path='like', permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        blog.like_the_content(request.user)
        return Response(data='liked', status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch', 'put'], detail=True, url_path='dislike', permission_classes=[IsAuthenticatedOrReadOnly])
    def un_like(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        blog.dislike_the_content(request.user)
        return Response(data='disliked', status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_likes(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        likes = blog.get_likes()
        return Response(data=likes, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-dislikes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_dislikes(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        dislikes = blog.get_dislike()
        return Response(data=dislikes, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-comments', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_comments(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        comments = blog.get_comments()
        serialize = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='common-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_common_liked_user(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        common_likes = blog.get_common_likes(request.user)
        serialize = UserSerializer(common_likes, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['patch'], detail=True, url_path='like', permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        review = Review.objects.get(pk=pk)
        review.like_the_content(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch', 'put'], detail=True, url_path='dislike', permission_classes=[IsAuthenticatedOrReadOnly])
    def un_like(self, request, pk=None):
        review = Review.objects.get(pk=pk)
        review.dislike_the_content(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_likes(self, request, pk=None):
        review = Review.objects.get(pk=pk)
        likes = review.get_likes()
        return Response(data={'likes': likes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-dislikes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_dislikes(self, request, pk=None):
        review = Review.objects.get(pk=pk)
        dislikes = review.get_dislike()
        return Response(data={'dislikes': dislikes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-comments', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_comments(self, request, pk=None):
        review = Review.objects.get(pk=pk)
        comments = review.get_comments()
        serialize = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='common-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_common_liked_user(self, request, pk=None):
        review = Review.objects.get(pk=pk)
        common_likes = review.get_common_likes(request.user)
        serialize = UserSerializer(common_likes, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class StatusVewSet(ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    # authentication_classes = [TokenAuthentication]
    queryset = Status.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['patch'], detail=True, url_path='like', permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        status_obj = Status.objects.get(pk=pk)
        status_obj.like_the_content(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch', 'put'], detail=True, url_path='dislike', permission_classes=[IsAuthenticatedOrReadOnly])
    def un_like(self, request, pk=None):
        status_obj = Status.objects.get(pk=pk)
        status_obj.dislike_the_content(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_likes(self, request, pk=None):
        status_obj = Status.objects.get(pk=pk)
        likes = status_obj.get_likes()
        return Response(data={'likes': likes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-dislikes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_dislikes(self, request, pk=None):
        status_obj = Status.objects.get(pk=pk)
        dislikes = status_obj.get_dislike()
        return Response(data={'dislikes': dislikes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-comments', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_comments(self, request, pk=None):
        status_obj = Status.objects.get(pk=pk)
        comments = status_obj.get_comments()
        serialize = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='common-likes', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_common_liked_user(self, request, pk=None):
        status_obj = Status.objects.get(pk=pk)
        common_likes = status_obj.get_common_likes(request.user)
        serialize = UserSerializer(common_likes, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)
