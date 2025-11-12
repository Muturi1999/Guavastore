
from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductListSerializer, ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """Cart item serializer"""
    
    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    product_id = serializers.IntegerField(write_only=True)
    variant_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'variant', 'product_id', 'variant_id',
            'quantity', 'price', 'subtotal', 'created_at'
        ]
        read_only_fields = ['id', 'price', 'subtotal', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    """Cart serializer"""
    
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = [
            'id', 'items', 'total_items', 'subtotal', 'total',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
