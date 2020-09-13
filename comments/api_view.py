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

    @action(methods=["patch"], detail=True, url_path='like', permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        comment = self.get_object()
        comment.like(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='dislike', permission_classes=[IsAuthenticatedOrReadOnly])
    def dislike(self, request, pk=None):
        comment = self.get_object()
        comment.dislike(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get-comments', permission_classes=[IsAuthenticatedOrReadOnly])
    def get_comments(self, request, pk=None):
        comment = self.get_object()
        comments = comment.get_comments()
        serialize = CommentSerializer(comments, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(edited=True)
