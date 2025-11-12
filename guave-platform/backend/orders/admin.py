from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory, ShippingMethod

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_email', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', 'payment_method']
    search_fields = ['order_number', 'customer_email', 'transaction_id', 'tracking_number']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'customer', 'customer_email', 'customer_phone', 'status')}),
        ('Shipping Address', {'fields': ('shipping_full_name', 'shipping_address_line1', 'shipping_address_line2', 
                                         'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country', 'shipping_phone')}),
        ('Billing Address', {'fields': ('billing_full_name', 'billing_address_line1', 'billing_address_line2',
                                        'billing_city', 'billing_state', 'billing_postal_code', 'billing_country')}),
        ('Order Totals', {'fields': ('subtotal', 'discount_amount', 'shipping_cost', 'tax_amount', 'total')}),
        ('Payment', {'fields': ('payment_method', 'payment_status', 'transaction_id', 'paid_at')}),
        ('Shipping', {'fields': ('shipping_method', 'tracking_number', 'carrier', 'shipped_at', 'delivered_at')}),
        ('Additional Info', {'fields': ('coupon_code', 'customer_notes', 'admin_notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'estimated_days_min', 'estimated_days_max', 'is_active', 'display_order']
    list_filter = ['is_active']
    search_fields = ['name']