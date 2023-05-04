from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import registration

urlpatterns = [
    path('users/', include('users.api_urls')),
    path('topics/', include('topics.api_urls')),
    path('suggestions/', include('suggestions.api_urls')),
    path('groups/', include('groups.api_urls')),
    path('contents/', include('contents.api_urls')),
    path('movies/', include('movies.api_urls')),
    path('persons/', include('persons.api_urls')),
    path('shares/', include('shares.api_urls')),
    path('comments/', include('comments.api_urls')),
    path('notifications/', include('notifications.api_urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', registration, name='register'),
]
