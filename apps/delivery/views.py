from django.utils import timezone
from rest_framework import viewsets

from .models import Delivery
from .serializers import DeliverySerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all().order_by("-created_at")
    serializer_class = DeliverySerializer

    def perform_update(self, serializer):
        delivery = serializer.save()

        if delivery.status == "delivered":
            delivery.delivered_at = timezone.now()
            delivery.save()

            delivery.order.status = "delivered"
            delivery.order.save()

        elif delivery.status == "out_for_delivery":
            delivery.order.status = "out_for_delivery"
            delivery.order.save()

        elif delivery.status == "assigned":
            delivery.order.status = "confirmed"
            delivery.order.save()