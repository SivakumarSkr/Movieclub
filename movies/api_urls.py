from rest_framework_nested import routers

from movies import api_view

# router = DefaultRouter()
router = routers.SimpleRouter()
router.register('movie', api_view.MovieViewSet, base_name='movie')
router.register('language', api_view.LanguageViewSet, base_name='language')
router.register('genre', api_view.GenreViewSet, base_name='genre')
router.register('rate', api_view.RatingViewSet, base_name='rate')
urlpatterns = [
]
urlpatterns += router.urls
