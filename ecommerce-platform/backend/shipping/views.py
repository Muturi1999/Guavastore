from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import (
    ShippingMethod, ShippingAddress, OrderShipping, OrderTracking
)
from .serializers import (
    ShippingMethodSerializer, ShippingAddressSerializer,
    OrderShippingSerializer, OrderTrackingSerializer
)
from datetime import timedelta, date

# --- Shipping Methods ---
class ShippingMethodListView(generics.ListAPIView):
    queryset = ShippingMethod.objects.filter(is_active=True)
    serializer_class = ShippingMethodSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['order_total'] = self.request.query_params.get('order_total', 0)
        return context


# --- Shipping Addresses ---
class ShippingAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- Select Shipping Method for Order ---
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def select_shipping_method(request):
    """
    Select shipping method during checkout.
    """
    order_id = request.data.get('order_id')
    address_id = request.data.get('address_id')
    method_id = request.data.get('method_id')
    order_total = float(request.data.get('order_total', 0))

    if not (order_id and address_id and method_id):
        return Response({'error': 'Missing fields'}, status=400)

    from .models import ShippingMethod, ShippingAddress, OrderShipping
    try:
        method = ShippingMethod.objects.get(pk=method_id)
        address = ShippingAddress.objects.get(pk=address_id, user=request.user)
    except (ShippingMethod.DoesNotExist, ShippingAddress.DoesNotExist):
        return Response({'error': 'Invalid data'}, status=404)

    est_delivery = date.today() + timedelta(days=method.estimated_days_max)

    shipping, created = OrderShipping.objects.update_or_create(
        order_id=order_id,
        defaults={
            'shipping_method': method,
            'shipping_address': address,
            'shipping_cost': method.get_cost(order_total),
            'estimated_delivery': est_delivery,
        }
    )

    serializer = OrderShippingSerializer(shipping)
    return Response(serializer.data)


# --- Order Tracking ---
class OrderTrackingDetailView(generics.RetrieveAPIView):
    queryset = OrderTracking.objects.all()
    serializer_class = OrderTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'tracking_number'
