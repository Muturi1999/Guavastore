from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductVariant, Tag


# -------------------
# Category serializers
# -------------------
class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    product_count = serializers.IntegerField(source='get_product_count', read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent', 
            'image', 'icon', 'is_active', 'order', 
            'meta_title', 'meta_description', 'children', 'product_count'
        ]

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data


# -------------------
# Brand serializers
# -------------------
class BrandSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'slug', 'logo', 'description', 
            'website', 'is_active', 'featured', 'product_count'
        ]


# -------------------
# ProductImage serializers
# -------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order', 'is_featured']


# -------------------
# ProductVariant serializers
# -------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'sku', 'attributes', 'price', 'final_price', 'stock_quantity', 'image', 'is_active']


# -------------------
# Product serializers
# -------------------
class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'barcode',
            'category', 'brand', 'price', 'compare_price',
            'discount_percentage', 'stock_quantity', 'stock_status',
            'is_active', 'is_featured', 'is_new', 'is_on_sale',
            'featured_image'
        ]


class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + [
            'description', 'short_description', 'specifications', 'meta_title', 
            'meta_description', 'meta_keywords', 'view_count', 'sold_count',
            'average_rating', 'review_count', 'images', 'variants', 'tags'
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# -------------------
# Tag serializers
# -------------------
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
