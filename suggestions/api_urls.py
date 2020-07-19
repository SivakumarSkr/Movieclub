from rest_framework.routers import DefaultRouter

from suggestions.api_view import SuggestionViewSet

router = DefaultRouter()
router.register('suggestion', SuggestionViewSet, base_name='topics')
urlpatterns = [
]
urlpatterns += router.urls
