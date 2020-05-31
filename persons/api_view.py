from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsPrime
from persons.models import Star
from persons.serializers import StarSerializer


class PersonViewSet(ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'country',)
    permission_classes = (IsAuthenticated, IsPrime)

    # authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, url_path='follow', methods=['patch', 'put'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        person = self.get_object()
        result = person.follow(request.user)
        if result:
            http_status = status.HTTP_202_ACCEPTED
        else:
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(status=http_status)

    @action(detail=True, methods=['patch', 'put'], url_path='un-follow', permission_classes=[IsAuthenticated])
    def un_follow(self, request, pk=None):
        person = self.get_object()
        result = person.un_follow(request.user)
        if result:
            http_status = status.HTTP_202_ACCEPTED
        else:
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(status=http_status)
