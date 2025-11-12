from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'product',
            'product_name',
            'customer',
            'customer_name',
            'rating',
            'title',
            'comment',
            'is_approved',
            'is_verified_purchase',
            'helpful_count',
            'created_at'
        ]
        read_only_fields = ['id', 'helpful_count', 'created_at']
