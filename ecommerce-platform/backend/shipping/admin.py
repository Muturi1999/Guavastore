# from django.contrib import admin
# from .models import ShippingMethod, ShippingZone, OrderTracking, TrackingEvent

# @admin.register(ShippingMethod)
# class ShippingMethodAdmin(admin.ModelAdmin):
#     list_display = [
#         'name', 'cost', 'estimated_days_min', 'estimated_days_max',
#         'free_shipping_threshold', 'is_active', 'order'
#     ]
#     list_filter = ['is_active']
#     search_fields = ['name', 'description']
#     ordering = ['order', 'cost']

# @admin.register(ShippingZone)
# class ShippingZoneAdmin(admin.ModelAdmin):
#     list_display = ['name', 'is_active']
#     list_filter = ['is_active']
#     search_fields = ['name']
#     filter_horizontal = ['methods']

# class TrackingEventInline(admin.TabularInline):
#     model = TrackingEvent
#     extra = 0

# @admin.register(OrderTracking)
# class OrderTrackingAdmin(admin.ModelAdmin):
#     list_display = [
#         'tracking_number', 'order', 'carrier', 'status',
#         'estimated_delivery', 'updated_at'
#     ]
#     list_filter = ['status', 'carrier']
#     search_fields = ['tracking_number', 'order__order_number']
#     readonly_fields = ['created_at', 'updated_at']
#     inlines = [TrackingEventInline]
