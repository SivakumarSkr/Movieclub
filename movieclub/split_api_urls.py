from django.urls import path, include

urlpatterns = [
    path('users/', include('users.api_urls')),
    path('topics/', include('topics.api_urls')),
    path('suggestions/', include('suggestions.api_urls')),
    path('groups/', include('groups.api_urls')),
    path('contents/', include('contents.api_urls')),
    path('movies/', include('movies.api_urls')),
    path('persons/', include('persons.api_urls')),
    path('shares/', include('shares.api_urls')),
]
