from rest_framework import serializers
from .models import (Category, Brand, Product, ProductImage, ProductAttribute,
                     ProductAttributeValue, ProductVariant, ProductSpecification,
                     ProductBadge, ProductBadgeAssignment)


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []


class BrandSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = '__all__'
    
    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = '__all__'


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    attribute_type = serializers.CharField(source='attribute.attribute_type', read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBadge
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    main_image = serializers.SerializerMethodField()
    discount_percentage = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    badges = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'sku', 'category_name', 'brand_name', 
                  'price', 'compare_price', 'discount_percentage', 'stock_status',
                  'main_image', 'average_rating', 'review_count', 'is_featured',
                  'is_new', 'badges']
    
    def get_main_image(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_image.image.url)
        return None
    
    def get_badges(self, obj):
        badges = obj.badge_assignments.filter(badge__is_active=True)
        return ProductBadgeSerializer([ba.badge for ba in badges], many=True).data


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    badges = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_badges(self, obj):
        badges = obj.badge_assignments.filter(badge__is_active=True)
        return ProductBadgeSerializer([ba.badge for ba in badges], many=True).data