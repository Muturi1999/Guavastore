from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from accounts.serializers import AddressSerializer
from products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer"""
    
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'variant_name', 'quantity', 'price', 'subtotal'
        ]
        read_only_fields = ['id', 'subtotal']

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Order status history serializer"""
    
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'notes', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    """Order list serializer"""
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'payment_status',
            'total', 'created_at'
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    """Order detail serializer"""
    
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    billing_address = AddressSerializer(read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'status', 'payment_status',
            'customer_email', 'customer_phone',
            'shipping_address', 'billing_address',
            'items', 'subtotal', 'shipping_cost', 'tax', 'discount', 'total',
            'payment_method', 'transaction_id',
            'customer_notes', 'status_history',
            'created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at'
        ]
        read_only_fields = [
            'id', 'order_number', 'created_at', 'updated_at',
            'paid_at', 'shipped_at', 'delivered_at'
        ]

class OrderCreateSerializer(serializers.Serializer):
    """Order creation serializer"""
    
    shipping_address_id = serializers.IntegerField()
    billing_address_id = serializers.IntegerField(required=False, allow_null=True)
    payment_method = serializers.ChoiceField(choices=[
        ('card', 'Credit/Debit Card'),
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    ])
    customer_notes = serializers.CharField(required=False, allow_blank=True)
    coupon_code = serializers.CharField(required=False, allow_blank=True)
