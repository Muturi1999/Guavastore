# from rest_framework import serializers
# from .models import Wishlist, WishlistItem
# from products.serializers import ProductListSerializer

# class WishlistItemSerializer(serializers.ModelSerializer):
#     """Wishlist item serializer"""
    
#     product = ProductListSerializer(read_only=True)
#     product_id = serializers.IntegerField(write_only=True)
    
#     class Meta:
#         model = WishlistItem
#         fields = ['id', 'product', 'product_id', 'added_at']
#         read_only_fields = ['id', 'added_at']

# class WishlistSerializer(serializers.ModelSerializer):
#     """Wishlist serializer"""
    
#     items = WishlistItemSerializer(many=True, read_only=True)
#     item_count = serializers.IntegerField(read_only=True)
    
#     class Meta:
#         model = Wishlist
#         fields = ['id', 'items', 'item_count', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']
