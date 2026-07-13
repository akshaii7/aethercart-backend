from django.db import models
from apps.products.models import Product
from apps.accounts.models import UserProfile


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True
    )

    customer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "No Product"
        customer_name = self.customer.name if self.customer else "Customer"
        return f"{customer_name} - {product_name} - {self.rating}"