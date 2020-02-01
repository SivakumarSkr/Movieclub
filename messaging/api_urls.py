from rest_framework.routers import DefaultRouter

from messaging import api_view

router = DefaultRouter()
router.register('message', api_view.MessageVewSet, base_name='message')
router.register('chat', api_view.GroupBlogViewSet, base_name='chat')
urlpatterns = [
]
urlpatterns += router.urls
