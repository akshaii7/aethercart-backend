from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from .serializers import CartItemSerializer
from apps.accounts.models import UserProfile


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_profile(self):
        user = self.request.user

        profile = UserProfile.objects.filter(user=user).first()
        if profile:
            return profile

        if user.email:
            profile = UserProfile.objects.filter(email=user.email).first()
            if profile:
                profile.user = user
                profile.save()
                return profile

        profile = UserProfile.objects.create(
            user=user,
            name=user.username,
            email=user.email or f"{user.username}_{user.id}@aethercart.local",
            role="customer"
        )

        return profile

    def get_queryset(self):
        profile = self.get_profile()
        return CartItem.objects.filter(customer=profile).order_by("-id")

    def perform_create(self, serializer):
        profile = self.get_profile()
        serializer.save(customer=profile)