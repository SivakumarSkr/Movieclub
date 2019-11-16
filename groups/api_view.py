from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from groups.models import Group, GroupBlog
from groups.permissions import IsOwner, IsOwnerBlog
from groups.serializers import GroupSerializer, GroupBlogSerializer


class GroupVewSet(ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    authentication_classes = [TokenAuthentication]
    search_fields = ('name', 'type_of_group')
    queryset = Group.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GroupBlogViewSet(ModelViewSet):
    serializer_class = GroupBlogSerializer
    queryset = GroupBlog.objects.all()
    permission_classes = (IsOwnerBlog,)
    authentication_classes = [TokenAuthentication]
    filter_backends = (SearchFilter, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
