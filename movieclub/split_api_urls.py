from django.urls import path, include

urlpatterns = [
    path('', include('users.api_urls')),
    path('', include('topics.api_urls')),
    path('', include('suggestions.api_urls')),
    path('', include('groups.api_urls')),
    path('', include('contents.api_urls')),
    path('', include('movies.api_urls')),
    path('', include('persons.api_urls')),
]
