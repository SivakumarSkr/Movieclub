from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api_view import UserLogin, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('login/', UserLogin.as_view()),
    path('', include(router.urls))
]
