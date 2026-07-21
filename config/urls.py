from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def redirect_to_frontend(request):
    return redirect('https://aethercart-frontend.vercel.app')

urlpatterns = [
    path('', redirect_to_frontend),
    path("admin/", admin.site.urls),

    path("api/accounts/", include("apps.accounts.urls")),
    path("api/products/", include("apps.products.urls")),
    path("api/cart/", include("apps.cart.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/delivery/", include("apps.delivery.urls")),
    path("api/payments/", include("apps.payments.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/reviews/", include("apps.reviews.urls")),
]

# Always serve media files (works in both development and on Render production)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)