from django.db import models
from apps.accounts.models import UserProfile
from apps.products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    RETURN_CHOICES = (
        ("none", "None"),
        ("requested", "Requested"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    )

    customer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )

    delivery_address = models.TextField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending",
    )

    return_status = models.CharField(
    max_length=20,
    choices=[
        ("none", "None"),
        ("requested", "Requested"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ],
    default="none",
)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"