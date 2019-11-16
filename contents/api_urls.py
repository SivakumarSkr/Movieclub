from django.urls import include, path
from rest_framework.routers import DefaultRouter

from contents import api_view

router = DefaultRouter()
router.register('answer', api_view.AnswerViewSet, base_name='answer')
router.register('blog', api_view.BlogViewSet, base_name='blog')
router.register('review', api_view.ReviewViewSet, base_name='review')
router.register('status', api_view.StatusVewSet, base_name='status')
urlpatterns = [
]
urlpatterns += router.urls
