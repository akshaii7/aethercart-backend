from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        default=""
    )

    address = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    role = serializers.CharField(
        write_only=True,
        required=False,
        default="customer"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "phone",
            "address",
            "role",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        address = validated_data.pop("address", "")
        role = validated_data.pop("role", "customer")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        UserProfile.objects.create(
            user=user,
            name=user.username,
            email=user.email,
            phone=phone,
            address=address,
            role=role,
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_profile_image_url(self, obj):
        request = self.context.get("request")

        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)

        return None