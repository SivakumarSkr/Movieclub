from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.models import Group, GroupBlog, ClosedGroup, JoinRequest
from groups.permissions import IsOwnerBlog, IsAdmin, IsCreator, IsMember, IsAuthorizer, IsRequestPermission
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
        group = self.queryset.get(pk=pk)
        group.join(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, url_path='leave', permission_classes=[IsMember])
    def leave(self, request, pk=None):
        group = self.queryset.get(pk=pk)
        group.leave(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='check-member', permission_classes=[IsMember])
    def check_member(self, request, pk=None):
        group = self.queryset.get(pk=pk)
        check = group.check_member(request.user)
        return Response(data={'data': check}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-members', permission_classes=[IsMember, IsCreator])
    def get_members(self, request, pk=None):
        group = self.queryset.get(pk=pk)
        followers = group.get_members()
        serialize = UserSerializer(followers, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class ClosedGroupViewSet(GroupVewSet):
    permission_classes = (IsCreator,)
    serializer_class = ClosedGroupSerializer
    # authentication_classes = [TokenAuthentication]
    queryset = ClosedGroup.objects.all()

    @action(methods=['get'], detail=True, url_path='get-admins', permission_classes=[IsAdmin])
    def get_admins(self, request, pk=None):
        status_code = status.HTTP_200_OK
        try:
            group = self.queryset.get(pk=pk)
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
            group = self.queryset.get(pk=pk)
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
        status_code = status.HTTP_200_OK
        try:
            user = User.objects.get(pk=request.GET.get('user', None))
            group = self.queryset.get(pk=pk)
        except ClosedGroup.DoesNotExist as e:
            data = {'detail': "This action is not applicable for open groups."}
            status_code = status.HTTP_400_BAD_REQUEST
        except User.DoesNotExist as e:
            data = {'detail': "Please provide valid user."}
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            group.remove_admin(user)
        return Response(data=data, status=status_code)

    def join(self, request, pk=None):
        pass


class JoinRequestViewSet(ModelViewSet):
    serializer_class = JoinRequestSerializer
    queryset = JoinRequest.objects.all()
    permission_classes = [IsRequestPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthorizer])
    def approve(self, request, pk=None):
        request_obj = self.queryset.get(pk=pk)
        request_obj.approve(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, permission_classes=[IsRequestPermission])
    def cancel(self, request, pk=None):
        request_obj = self.queryset.get(pk=pk)
        request_obj.cancel(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class GroupBlogViewSet(ModelViewSet):
    serializer_class = GroupBlogSerializer
    queryset = GroupBlog.objects.all()
    permission_classes = (IsOwnerBlog,)
    authentication_classes = [TokenAuthentication]
    filter_backends = (SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
