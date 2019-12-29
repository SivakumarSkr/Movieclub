from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from topics.models import Topic
from topics.permissions import TopicPermission
from topics.serializers import TopicSerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (TopicPermission, IsAuthenticatedOrReadOnly)
    filter_backends = (SearchFilter, )
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=['patch'], detail=True)
    def follow(self, request, pk=None):
        topic = Topic.objects.get(pk=pk)
        topic.follow_the_topic(request.user)
        return Response(data='Now you are following {}'.format(topic.head), status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True)
    def un_follow(self, request, pk=None):
        topic = Topic.objects.get(pk=pk)
        topic.un_follow_the_topic(self.request.user)
        return Response(data="Now you are not following {}".format(topic.head), status=status.HTTP_200_OK)
