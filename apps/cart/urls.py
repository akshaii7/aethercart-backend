from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register("items", CartItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
]