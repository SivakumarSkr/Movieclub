from django.urls import include, path
from rest_framework.routers import DefaultRouter

from groups import api_view

router = DefaultRouter()
router.register('groups', api_view.GroupVewSet, base_name='group')
router.register('group_blog', api_view.GroupBlogViewSet, base_name='group_blog')
urlpatterns = [
]
urlpatterns += router.urls
