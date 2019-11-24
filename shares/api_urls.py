from rest_framework.routers import DefaultRouter

from shares import api_view

router = DefaultRouter()
router.register('share', api_view.ShareViewSet, base_name='share')

urlpatterns = [
]
urlpatterns += router.urls
