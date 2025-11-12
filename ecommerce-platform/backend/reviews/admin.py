# from django.contrib import admin
# from .models import Review, ReviewImage, ReviewHelpful

# class ReviewImageInline(admin.TabularInline):
#     model = ReviewImage
#     extra = 0

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = [
#         'product', 'user', 'rating', 'is_verified_purchase',
#         'is_approved', 'helpful_count', 'created_at'
#     ]
#     list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
#     search_fields = ['product__name', 'user__email', 'title', 'comment']
#     readonly_fields = ['helpful_count', 'created_at', 'updated_at']
#     inlines = [ReviewImageInline]
    
#     fieldsets = (
#         ('Review Details', {
#             'fields': ('product', 'user', 'order', 'rating', 'title', 'comment')
#         }),
#         ('Status', {
#             'fields': ('is_verified_purchase', 'is_approved', 'helpful_count')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/shipping/', include('shipping.urls')),
]
