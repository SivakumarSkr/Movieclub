from rest_framework.routers import DefaultRouter

from comments import api_view

router = DefaultRouter()
router.register('comments', api_view.CommentViewSet, base_name='comments', )

urlpatterns = [
]
urlpatterns += router.urls
