from rest_framework_nested import routers

from notifications import api_view

# router = DefaultRouter()
router = routers.SimpleRouter()
router.register('notifications', api_view.NotificationNewViewSet, base_name='notification')
urlpatterns = [
]
urlpatterns += router.urls
