from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductVariant, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'featured']
    list_filter = ['is_active', 'featured']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'category', 'brand', 'price',
        'stock_quantity', 'is_active', 'is_featured'
    ]
    list_filter = [
        'is_active', 'is_featured', 'is_new', 'is_on_sale',
        'category', 'brand', 'stock_status'
    ]
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ['view_count', 'sold_count', 'average_rating', 'review_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'barcode', 'category', 'brand')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'specifications')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'stock_status', 'low_stock_threshold')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_new', 'is_on_sale')
        }),
        ('Statistics', {
            'fields': ('view_count', 'sold_count', 'average_rating', 'review_count'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}