from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")
router.register("items", OrderItemViewSet, basename="order-items")

urlpatterns = [
    path("", include(router.urls)),
]