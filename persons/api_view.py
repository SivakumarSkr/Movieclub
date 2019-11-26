from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from persons.models import Star
from persons.permissions import StarPermission
from persons.serializers import StarSerializer


class PersonViewSet(ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'country', )
    permission_classes = (StarPermission,)
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, url_path='follow/(?P<pk>[^/.]+)', methods=['put'])
    def follow(self, request, pk=None):
        person = Star.objects.get(pk=pk)
        person.follow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED, data='Now you following {}'.format(request.user))

    @action(detail=False, methods=['put'], url_path='un_follow/(?P<pk>[^/.]+)')
    def un_follow(self, request, pk=None):
        person = Star.objects.get(pk=pk)
        person.unfollow(request.user)
        return Response(status=status.HTTP_202_ACCEPTED, data='You are not following {}.'.format(request.user))
