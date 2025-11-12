from django.urls import path
from .views import CartView, CartItemView, ApplyCouponView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items/', CartItemView.as_view(), name='cart_add_item'),
    path('items/<int:pk>/', CartItemView.as_view(), name='cart_item_detail'),
    path('coupon/', ApplyCouponView.as_view(), name='apply_coupon'),
]