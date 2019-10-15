from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from persons.models import Star
from persons.serializers import StarSerializer


class PersonViewSet(ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'country', )
    authentication_classes = [TokenAuthentication]
