from rest_framework.routers import DefaultRouter

from persons import api_view

router = DefaultRouter()
router.register('stars', api_view.PersonViewSet, base_name='star')
urlpatterns = [
]
urlpatterns += router.urls
