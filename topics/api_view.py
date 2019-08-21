from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from topics.models import Topic
from topics.permissions import TopicPermission
from topics.serializers import TopicSerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (TopicPermission,)
    filter_backends = (SearchFilter, )
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
