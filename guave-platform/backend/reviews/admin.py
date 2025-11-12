from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'customer',
        'rating',
        'title',
        'is_approved',
        'is_verified_purchase',
        'helpful_count',
        'created_at'
    )
    list_filter = ('rating', 'is_approved', 'is_verified_purchase', 'created_at')
    search_fields = ('title', 'comment', 'customer__name', 'product__name')
    readonly_fields = ('created_at', 'helpful_count')
