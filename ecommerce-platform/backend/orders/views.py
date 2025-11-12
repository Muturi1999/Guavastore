
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Order, OrderItem, OrderStatusHistory
from cart.models import Cart
from accounts.models import Address
from .serializers import (
    OrderSerializer, OrderDetailSerializer,
    OrderCreateSerializer, OrderStatusHistorySerializer
)

class OrderListView(generics.ListAPIView):
    """List user orders"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Search by order number
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(order_number__icontains=search)
        
        return queryset.order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    """Get order details"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer
    lookup_field = 'order_number'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCreateView(APIView):
    """Create order from cart"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Get cart
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not cart.items.exists():
            return Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get addresses
        shipping_address = get_object_or_404(
            Address,
            id=serializer.validated_data['shipping_address_id'],
            user=user
        )
        
        billing_address_id = serializer.validated_data.get('billing_address_id')
        billing_address = None
        if billing_address_id:
            billing_address = get_object_or_404(
                Address,
                id=billing_address_id,
                user=user
            )
        else:
            billing_address = shipping_address
        
        # Calculate totals
        subtotal = cart.subtotal
        shipping_cost = 0  # Calculate based on shipping method
        tax = 0  # Calculate based on location
        discount = 0
        
        # Apply coupon if provided
        coupon_code = serializer.validated_data.get('coupon_code')
        if coupon_code:
            from core.models import Coupon
            try:
                coupon = Coupon.objects.get(code__iexact=coupon_code)
                if coupon.is_valid():
                    discount = coupon.calculate_discount(subtotal)
                    coupon.usage_count += 1
                    coupon.save()
            except Coupon.DoesNotExist:
                pass
        
        total = subtotal + shipping_cost + tax - discount
        
        # Create order
        order = Order.objects.create(
            user=user,
            customer_email=user.email,
            customer_phone=user.phone,
            shipping_address=shipping_address,
            billing_address=billing_address,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            discount=discount,
            total=total,
            payment_method=serializer.validated_data['payment_method'],
            customer_notes=serializer.validated_data.get('customer_notes', ''),
            status='pending',
            payment_status='pending'
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                quantity=cart_item.quantity,
                price=cart_item.price
            )
            
            # Update product stock
            if cart_item.variant:
                cart_item.variant.stock_quantity -= cart_item.quantity
                cart_item.variant.save()
            else:
                cart_item.product.stock_quantity -= cart_item.quantity
                cart_item.product.save()
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            notes='Order created',
            created_by=user
        )
        
        # Clear cart
        cart.items.all().delete()
        
        # Return order details
        response_serializer = OrderDetailSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CancelOrderView(APIView):
    """Cancel order"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, order_number):
        order = get_object_or_404(
            Order,
            order_number=order_number,
            user=request.user
        )
        
        if order.status not in ['pending', 'confirmed']:
            return Response({
                'error': 'Order cannot be cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            status='cancelled',
            notes='Cancelled by customer',
            created_by=request.user
        )
        
        # Restore stock
        for item in order.items.all():
            if item.variant:
                item.variant.stock_quantity += item.quantity
                item.variant.save()
            else:
                item.product.stock_quantity += item.quantity
                item.product.save()
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)