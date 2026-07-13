from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

from apps.cart.models import CartItem
from apps.accounts.models import UserProfile
from apps.notifications.models import Notification
from apps.products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
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
            role="customer",
        )

        return profile

    def get_queryset(self):
        profile = self.get_profile()
        return Order.objects.filter(customer=profile).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        profile = self.get_profile()

        delivery_address = request.data.get("delivery_address")
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        # -----------------------------
        # BUY NOW
        # -----------------------------
        if product_id:

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            total_amount = product.price * quantity

            order = Order.objects.create(
                customer=profile,
                delivery_address=delivery_address,
                total_amount=total_amount,
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

            Notification.objects.create(
                user=profile,
                title="Order Placed",
                message=f"Your order #{order.id} has been placed successfully.",
            )

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # -----------------------------
        # CART CHECKOUT
        # -----------------------------
        cart_items = CartItem.objects.filter(customer=profile)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = Order.objects.create(
            customer=profile,
            delivery_address=delivery_address,
            total_amount=0,
        )

        total_amount = 0

        for item in cart_items:
            item_total = item.product.price * item.quantity
            total_amount += item_total

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        order.total_amount = total_amount
        order.save()

        Notification.objects.create(
            user=profile,
            title="Order Placed",
            message=f"Your order #{order.id} has been placed successfully.",
        )

        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def request_return(self, request, pk=None):

        order = self.get_object()

        if order.status != "delivered":
            return Response(
                {"error": "Only delivered orders can be returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.return_status != "none":
            return Response(
                {"error": "Return request already submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.return_status = "requested"
        order.save()

        Notification.objects.create(
            user=order.customer,
            title="Return Requested",
            message=f"Return request submitted for Order #{order.id}",
        )

        return Response(
            {"message": "Return request submitted successfully."},
            status=status.HTTP_200_OK,
        )


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer