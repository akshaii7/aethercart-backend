from django.db import models


class Payment(models.Model):
    PAYMENT_STATUS = (
        ("created", "Created"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="created"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"