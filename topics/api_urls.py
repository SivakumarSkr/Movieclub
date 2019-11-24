from rest_framework.routers import DefaultRouter

from topics.api_view import TopicViewSet

router = DefaultRouter()
router.register('topic', TopicViewSet, base_name='topics')

urlpatterns = [
]
urlpatterns += router.urls
