from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserProfileViewSet, register_user

router = DefaultRouter()
router.register("profiles", UserProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register_user),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]