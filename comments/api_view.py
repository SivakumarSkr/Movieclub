from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comments.models import Comment
from comments.permissions import CommentPermission
from comments.serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission, IsAuthenticatedOrReadOnly)
    # authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["patch"], detail=True, url_path='like')
    def like(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.like_the_comment(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='dislike')
    def dislike_the_comment(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.dislike_the_comment(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get-likes')
    def get_likes(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        likes = comment.get_no_likes()
        return Response(data={'likes': likes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-dislikes')
    def get_dislikes(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        dislikes = comment.get_no_dislikes()
        return Response(data={'dislikes': dislikes}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-comments')
    def get_comments(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comments = comment.get_comments()
        serialize = CommentSerializer(comments, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(edited=True)
