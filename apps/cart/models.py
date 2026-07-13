from django.db import models
from apps.accounts.models import UserProfile
from apps.products.models import Product


class CartItem(models.Model):

    customer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.product.name} x {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity