from django.contrib import admin
from .models import (Category, Brand, Product, ProductImage, ProductAttribute,
                     ProductAttributeValue, ProductVariant, ProductSpecification,
                     ProductBadge, ProductBadgeAssignment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'display_order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_featured', 'is_active']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'brand', 'price', 'stock_quantity', 'stock_status', 'is_active']
    list_filter = ['category', 'brand', 'stock_status', 'is_featured', 'is_active']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSpecificationInline]
    readonly_fields = ['views_count', 'sales_count']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_main', 'display_order']
    list_filter = ['is_main']

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'attribute_type', 'display_order']
    list_filter = ['attribute_type']

@admin.register(ProductBadge)
class ProductBadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'text', 'is_active']
    list_filter = ['badge_type', 'is_active']