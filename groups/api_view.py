from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.models import Group, GroupBlog, ClosedGroup, JoinRequest
from groups.permissions import IsOwner, IsAdmin, IsCreator, IsMember, IsGroupAuthorizer, IsRequestPermission
from groups.serializers import GroupSerializer, GroupBlogSerializer, JoinRequestSerializer, ClosedGroupSerializer
from users.serializers import UserSerializer

User = get_user_model()


class GroupVewSet(ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsCreator,)
    # authentication_classes = [TokenAuthentication]
    search_fields = ('name',)
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        group = self.get_object()
        group.join(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, url_path='leave', permission_classes=[IsMember])
    def leave(self, request, pk=None):
        group = self.get_object()
        group.leave(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-members', permission_classes=[IsMember, IsCreator])
    def get_members(self, request, pk=None):
        group = self.get_object()
        followers = group.get_members()
        serialize = UserSerializer(followers, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class ClosedGroupViewSet(GroupVewSet):
    serializer_class = ClosedGroupSerializer
    # authentication_classes = [TokenAuthentication]
    queryset = ClosedGroup.objects.all()

    @action(methods=['get'], detail=True, url_path='get-admins', permission_classes=[IsAdmin])
    def get_admins(self, request, pk=None):
        status_code = status.HTTP_200_OK
        try:
            group = self.get_object()
        except ClosedGroup.DoesNotExist as e:
            data = {'detail': "This action is not applicable for open groups."}
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            admins = group.get_admins()
            serialize = UserSerializer(admins, many=True)
            data = serialize.data
        return Response(data=data, status=status_code)

    @action(methods=['patch'], detail=True, url_path='add-admin', permission_classes=[IsCreator])
    def add_admin(self, request, pk=None):
        data = {}
        status_code = status.HTTP_200_OK
        try:
            user = User.objects.get(pk=request.query_params.get('user', None))
            group = self.get_object()
        except ClosedGroup.DoesNotExist as e:
            data = {'detail': "This action is not applicable for open groups."}
            status_code = status.HTTP_400_BAD_REQUEST
        except User.DoesNotExist as e:
            data = {'detail': "Please provide valid user."}
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            group.add_admin(user)
        return Response(data=data, status=status_code)

    @action(methods=['patch'], detail=True, url_path='remove-admin', permission_classes=[IsCreator])
    def remove_admin(self, request, pk=None):
        data = {}
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            user = User.objects.get(pk=request.GET.get('user', None))
            group = self.get_object()
        except ClosedGroup.DoesNotExist as e:
            data = {'detail': "This action is not applicable for open groups."}
        except User.DoesNotExist as e:
            data = {'detail': "Please provide valid user."}
        else:
            group.remove_admin(user)
            status_code = status.HTTP_200_OK
        return Response(data=data, status=status_code)

    @action(methods=['patch'], detail=True, url_path='join', permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        group = self.get_object()
        JoinRequest.objects.create(user=request.user, group=group)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='get-common-members', permission_classes=[IsAuthenticated])
    def get_common_members(self, request, pk=None):
        group = self.get_object()
        users = group.get_common_members(request.user)
        serialize = UserSerializer(users, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='remove-member', permission_classes=[IsGroupAuthorizer])
    def remove_member(self, request, pk=None):
        group = self.get_object()
        is_member = group.remove_member(request.user)
        if is_member:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JoinRequestViewSet(ModelViewSet):
    serializer_class = JoinRequestSerializer
    queryset = JoinRequest.objects.all()
    permission_classes = [IsRequestPermission]

    @action(methods=['patch'], detail=True, permission_classes=[IsGroupAuthorizer])
    def approve(self, request, pk=None):
        request_obj = self.get_object()
        request_obj.approve(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, permission_classes=[IsOwner | IsGroupAuthorizer])
    def cancel(self, request):
        request_obj = self.get_object()
        request_obj.cancel(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class GroupBlogViewSet(ModelViewSet):
    serializer_class = GroupBlogSerializer
    queryset = GroupBlog.objects.all()
    permission_classes = (IsOwner,)
    authentication_classes = [TokenAuthentication]
    filter_backends = (SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['patch', 'update'], detail=True, url_path="approve", permission_classes=[IsGroupAuthorizer])
    def approve(self, request, pk=None):
        blog = self.get_object()
        blog.approve()
        return Response(status=status.HTTP_200_OK)
