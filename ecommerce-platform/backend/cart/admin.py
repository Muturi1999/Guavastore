from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['price', 'subtotal']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'subtotal', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'session_key']
    inlines = [CartItemInline]
    readonly_fields = ['total_items', 'subtotal', 'total']