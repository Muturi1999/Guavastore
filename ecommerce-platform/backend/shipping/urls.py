from django.urls import path
from . import views

urlpatterns = [
    path('methods/', views.ShippingMethodListView.as_view(), name='shipping-methods'),
    path('addresses/', views.ShippingAddressListCreateView.as_view(), name='shipping-addresses'),
    path('select/', views.select_shipping_method, name='select-shipping'),
    path('track/<str:tracking_number>/', views.OrderTrackingDetailView.as_view(), name='order-tracking'),
]
