from django.urls import path, include
from rest_framework.routers import DefaultRouter

from topics.api_view import TopicViewSet

router = DefaultRouter()
router.register('topic', TopicViewSet, base_name='topics')

urlpatterns = [
    path('topics/', include(router.urls))
]
