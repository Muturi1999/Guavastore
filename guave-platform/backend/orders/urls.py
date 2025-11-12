from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    OrderViewSet,
    OrderItemViewSet,
    OrderStatusHistoryViewSet,
    ShippingMethodViewSet,
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'order-status-history', OrderStatusHistoryViewSet, basename='orderstatushistory')
router.register(r'shipping-methods', ShippingMethodViewSet, basename='shippingmethod')

urlpatterns = [
    path('', include(router.urls)),
]
