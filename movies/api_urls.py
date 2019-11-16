from django.urls import include, path
from rest_framework.routers import DefaultRouter

from movies import api_view

router = DefaultRouter()
router.register('movie', api_view.MovieViewSet, base_name='movie')
router.register('language', api_view.LanguageViewSet, base_name='language')
router.register('genre', api_view.GenreViewSet, base_name='genre')
router.register('rate', api_view.RatingViewSet, base_name='rate')
urlpatterns = [
]
urlpatterns += router.urls
