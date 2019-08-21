from django.urls import path, include

urlpatterns = [
    path('', include('users.api_urls')),
    path('', include('topics.api_urls')),
]
