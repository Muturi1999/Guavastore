from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'subtotal']

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['status', 'notes', 'created_by', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'status', 'payment_status',
        'total', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at', 'payment_method']
    search_fields = ['order_number', 'user__email', 'customer_email']
    readonly_fields = [
        'order_number', 'created_at', 'updated_at',
        'paid_at', 'shipped_at', 'delivered_at'
    ]
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Customer Details', {
            'fields': ('customer_email', 'customer_phone')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total')
        }),
        ('Payment', {
            'fields': ('payment_method', 'transaction_id')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change:
            # Track status changes
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                OrderStatusHistory.objects.create(
                    order=obj,
                    status=obj.status,
                    notes=f'Status changed from {old_obj.status} to {obj.status}',
                    created_by=request.user
                )
        super().save_model(request, obj, form, change)
