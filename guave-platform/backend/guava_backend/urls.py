"""
URL configuration for guava_backend project.

The `urlpatterns` list routes URLs to views.
For more information, see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# DRF & Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ---- API Documentation setup ----
schema_view = get_schema_view(
    openapi.Info(
        title="Guava E-commerce API",
        default_version='v1',
        description="Comprehensive API documentation for the Guava e-commerce platform.",
        contact=openapi.Contact(email="support@guava.com"),
        license=openapi.License(name="Malipo License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# ---- URL Patterns ----
urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # API routes (modular apps)
    path("api/content/", include("content.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/customers/", include("customers.urls")),
    path("api/inventory/", include("inventory.urls")),   # fixed: was `include('include.urls')`
    path("api/notifications/", include("notifications.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/products/", include("products.urls")),
    path("api/promotions/", include("promotions.urls")),
    path("api/reviews/", include("reviews.urls")),

    # API documentation (Swagger + ReDoc)
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# ---- Static & Media during development ----
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
