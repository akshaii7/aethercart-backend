import razorpay

from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by("-id")
    serializer_class = PaymentSerializer


class CreatePaymentView(APIView):
    def post(self, request):
        amount = request.data.get("amount")

        if not amount:
            return Response(
                {"error": "Amount is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount_in_paise = int(float(amount) * 100)

            client = razorpay.Client(
                auth=(
                    settings.RAZORPAY_KEY_ID,
                    settings.RAZORPAY_KEY_SECRET
                )
            )

            razorpay_order = client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1
            })

            payment = Payment.objects.create(
                razorpay_order_id=razorpay_order["id"],
                amount=amount,
                status="created"
            )

            return Response({
                "payment_db_id": payment.id,
                "razorpay_order_id": razorpay_order["id"],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": amount_in_paise,
                "currency": "INR",
            })

        except Exception as error:
            return Response(
                {
                    "error": "Unable to create Razorpay order",
                    "details": str(error)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyPaymentView(APIView):
    def post(self, request):
        payment_db_id = request.data.get("payment_db_id")
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        if not payment_db_id:
            return Response(
                {"error": "Payment DB ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            })

            payment = Payment.objects.get(id=payment_db_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = "success"
            payment.save()

            return Response({
                "message": "Payment verified successfully",
                "status": "success"
            })

        except Exception as error:
            payment = Payment.objects.filter(id=payment_db_id).first()

            if payment:
                payment.status = "failed"
                payment.save()

            return Response(
                {
                    "error": "Payment verification failed",
                    "details": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )