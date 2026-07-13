from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    product_image = serializers.ImageField(
        source="product.image",
        read_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "customer",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.total_price()