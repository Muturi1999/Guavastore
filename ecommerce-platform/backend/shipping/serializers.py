
# from rest_framework import serializers
# from .models import ShippingMethod, OrderTracking, TrackingEvent

# class ShippingMethodSerializer(serializers.ModelSerializer):
#     """Shipping method serializer"""
    
#     calculated_cost = serializers.SerializerMethodField()
#     estimated_delivery = serializers.SerializerMethodField()
    
#     class Meta:
#         model = ShippingMethod
#         fields = [
#             'id', 'name', 'description', 'cost', 'calculated_cost',
#             'estimated_days_min', 'estimated_days_max',
#             'estimated_delivery', 'free_shipping_threshold'
#         ]
    
#     def get_calculated_cost(self, obj):
#         order_total = self.context.get('order_total', 0)
#         return obj.get_cost(order_total)
    
#     def get_estimated_delivery(self, obj):
#         from datetime import datetime, timedelta
#         min_date = datetime.now() + timedelta(days=obj.estimated_days_min)
#         max_date = datetime.now() + timedelta(days=obj.estimated_days_max)
#         return {
#             'min': min_date.date(),
#             'max': max_date.date()
#         }

# class TrackingEventSerializer(serializers.ModelSerializer):
#     """Tracking event serializer"""
    
#     class Meta:
#         model = TrackingEvent
#         fields = ['id', 'status', 'location', 'description', 'event_time']

# class OrderTrackingSerializer(serializers.ModelSerializer):
#     """Order tracking serializer"""
    
#     events = TrackingEventSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = OrderTracking
#         fields = [
#             'id', 'tracking_number', 'carrier', 'status',
#             'current_location', 'estimated_delivery',
#             'notes', 'events', 'updated_at'
#         ]

from rest_framework import serializers
from .models import (
    ShippingMethod, ShippingAddress, OrderShipping, OrderTracking, TrackingEvent
)

class ShippingMethodSerializer(serializers.ModelSerializer):
    calculated_cost = serializers.SerializerMethodField()
    estimated_delivery = serializers.SerializerMethodField()

    class Meta:
        model = ShippingMethod
        fields = [
            'id', 'name', 'description', 'cost', 'calculated_cost',
            'estimated_days_min', 'estimated_days_max',
            'estimated_delivery', 'free_shipping_threshold'
        ]

    def get_calculated_cost(self, obj):
        order_total = self.context.get('order_total', 0)
        return obj.get_cost(order_total)

    def get_estimated_delivery(self, obj):
        return obj.get_estimated_delivery_window()


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class OrderShippingSerializer(serializers.ModelSerializer):
    shipping_method = ShippingMethodSerializer()
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = OrderShipping
        fields = '__all__'


class TrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingEvent
        fields = ['id', 'status', 'location', 'description', 'event_time']


class OrderTrackingSerializer(serializers.ModelSerializer):
    events = TrackingEventSerializer(many=True, read_only=True)

    class Meta:
        model = OrderTracking
        fields = [
            'id', 'tracking_number', 'carrier', 'status',
            'current_location', 'estimated_delivery',
            'notes', 'events', 'updated_at'
        ]
