# from django.contrib import admin
# from .models import (
#     RecentlyViewed, ProductComparison,
#     Newsletter, Coupon, SEOMetadata
# )

# @admin.register(RecentlyViewed)
# class RecentlyViewedAdmin(admin.ModelAdmin):
#     list_display = ['product', 'user', 'session_key', 'viewed_at']
#     list_filter = ['viewed_at']
#     search_fields = ['product__name', 'user__email']

# @admin.register(ProductComparison)
# class ProductComparisonAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'session_key', 'updated_at']
#     list_filter = ['created_at', 'updated_at']
#     filter_horizontal = ['products']

# @admin.register(Newsletter)
# class NewsletterAdmin(admin.ModelAdmin):
#     list_display = ['email', 'is_active', 'subscribed_at', 'unsubscribed_at']
#     list_filter = ['is_active', 'subscribed_at']
#     search_fields = ['email']

# @admin.register(Coupon)
# class CouponAdmin(admin.ModelAdmin):
#     list_display = [
#         'code', 'discount_type', 'discount_value',
#         'usage_count', 'usage_limit', 'valid_from', 'valid_to', 'is_active'
#     ]
#     list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_to']
#     search_fields = ['code', 'description']
#     readonly_fields = ['usage_count', 'created_at', 'updated_at']
    
#     fieldsets = (
#         ('Coupon Details', {
#             'fields': ('code', 'description', 'discount_type', 'discount_value')
#         }),
#         ('Conditions', {
#             'fields': (
#                 'min_purchase_amount', 'max_discount_amount',
#                 'usage_limit', 'usage_count'
#             )
#         }),
#         ('Validity', {
#             'fields': ('valid_from', 'valid_to', 'is_active')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

# @admin.register(SEOMetadata)
# class SEOMetadataAdmin(admin.ModelAdmin):
#     list_display = ['page_type', 'page_slug', 'meta_title', 'is_active']
#     list_filter = ['page_type', 'is_active']
#     search_fields = ['page_slug', 'meta_title', 'meta_description']
    
#     fieldsets = (
#         ('Page Information', {
#             'fields': ('page_type', 'page_slug', 'is_active')
#         }),
#         ('Meta Tags', {
#             'fields': ('meta_title', 'meta_description', 'meta_keywords')
#         }),
#         ('Open Graph', {
#             'fields': ('og_title', 'og_description', 'og_image'),
#             'classes': ('collapse',)
#         }),
#         ('Advanced', {
#             'fields': ('schema_markup', 'canonical_url'),
#             'classes': ('collapse',)
#         }),
#     )