from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "customer", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["comment", "customer__name", "product__name"]