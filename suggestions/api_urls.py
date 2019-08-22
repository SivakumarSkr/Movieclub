from django.urls import path, include
from rest_framework.routers import DefaultRouter

from suggestions.api_view import SuggestionViewSet

router = DefaultRouter()
router.register('suggestion', SuggestionViewSet, base_name='topics')

urlpatterns = [
    path('suggestion/', include(router.urls))
]
