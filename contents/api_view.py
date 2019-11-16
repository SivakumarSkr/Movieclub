from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from contents.models import Answer, Blog, Review, Status
from contents.permissions import IsOwner
from contents.serializers import AnswerSerializer, BlogSerializer, ReviewSerializer, StatusSerializer


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    authentication_classes = [TokenAuthentication]
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    authentication_classes = [TokenAuthentication]
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StatusVewSet(ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)
    authentication_classes = [TokenAuthentication]
    queryset = Status.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

