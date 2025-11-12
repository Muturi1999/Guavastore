from rest_framework import viewsets, permissions
from .models import Order, OrderItem, OrderStatusHistory, ShippingMethod
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderStatusHistorySerializer,
    ShippingMethodSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('customer')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related('order', 'product')
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderStatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderStatusHistory.objects.all().select_related('order', 'created_by')
    serializer_class = OrderStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.filter(is_active=True)
    serializer_class = ShippingMethodSerializer
    permission_classes = [permissions.AllowAny]
