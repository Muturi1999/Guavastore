from rest_framework import serializers
from .models import Customer, Address, Wishlist, CustomerNote

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CustomerNoteSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CustomerNote
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'customer', 'product', 'product_name', 'created_at']


class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    notes = CustomerNoteSerializer(many=True, read_only=True)
    wishlists = WishlistSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth',
            'customer_type', 'email_marketing', 'email_orders', 'email_promotions',
            'total_orders', 'total_spent', 'average_order_value', 'loyalty_points',
            'created_at', 'updated_at', 'last_login_at', 'addresses', 'notes', 'wishlists'
        ]
