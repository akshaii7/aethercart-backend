from django.db import models
from django.utils import timezone

from apps.orders.models import Order
from apps.accounts.models import UserProfile


class Delivery(models.Model):
    STATUS_CHOICES = (
        ("assigned", "Assigned"),
        ("picked_up", "Picked Up"),
        ("out_for_delivery", "Out For Delivery"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    driver = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="assigned",
    )

    current_location = models.CharField(max_length=255, blank=True)

    delivered_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status == "assigned":
            self.order.status = "confirmed"

        elif self.status == "out_for_delivery":
            self.order.status = "out_for_delivery"

        elif self.status == "delivered":
            self.order.status = "delivered"

            if not self.delivered_at:
                self.delivered_at = timezone.now()
                super().save(update_fields=["delivered_at"])

        self.order.save(update_fields=["status"])

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"