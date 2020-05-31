from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwner
from topics.models import Topic
from topics.serializers import TopicSerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    filter_backends = (SearchFilter,)
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=['patch'], detail=True, url_path='follow', permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        topic = self.get_object()
        topic.follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='un-follow', permission_classes=[IsAuthenticated])
    def un_follow(self, request, pk=None):
        topic = self.get_object()
        result = topic.un_follow(self.request.user)
        if result:
            http_status = status.HTTP_202_ACCEPTED
        else:
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(status=http_status)
