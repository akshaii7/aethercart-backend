from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Review
from .serializers import ReviewSerializer
from apps.accounts.models import UserProfile


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all().order_by("-created_at")

        product_id = self.request.query_params.get("product")

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset

    def perform_create(self, serializer):
        profile = None

        if self.request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=self.request.user).first()

            if not profile:
                profile = UserProfile.objects.create(
                    user=self.request.user,
                    name=self.request.user.username,
                    email=self.request.user.email or f"{self.request.user.username}@aethercart.local",
                    role="customer",
                )

        serializer.save(customer=profile)