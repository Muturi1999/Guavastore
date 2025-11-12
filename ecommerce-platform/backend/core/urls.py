# from django.urls import path
# from .views import (
#     RecentlyViewedView, AddRecentlyViewedView,
#     CompareListView, AddToCompareView, RemoveFromCompareView,
#     NewsletterSubscribeView
# )

# app_name = 'core'

# urlpatterns = [
#     # Recently Viewed
#     path('recently-viewed/', RecentlyViewedView.as_view(), name='recently_viewed'),
#     path('recently-viewed/add/', AddRecentlyViewedView.as_view(), name='add_recently_viewed'),
    
#     # Comparison
#     path('compare/', CompareListView.as_view(), name='compare_list'),
#     path('compare/add/', AddToCompareView.as_view(), name='add_to_compare'),
#     path('compare/remove/<int:product_id>/', RemoveFromCompareView.as_view(), name='remove_from_compare'),
    
#     # Newsletter
#     path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
# ]

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
