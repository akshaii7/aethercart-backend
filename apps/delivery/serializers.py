from rest_framework import serializers
from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source="driver.name", read_only=True)

    class Meta:
        model = Delivery
        fields = "__all__"