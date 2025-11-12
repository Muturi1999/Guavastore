
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )

# urlpatterns = [
#     # Admin
#     path('admin/', admin.site.urls),
    
#     # API Documentation
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
#     # API Endpoints
#     path('api/auth/', include('accounts.urls')),
#     path('api/products/', include('products.urls')),
#     path('api/orders/', include('orders.urls')),
#     path('api/cart/', include('cart.urls')),
#     path('api/reviews/', include('reviews.urls')),
#     path('api/wishlist/', include('wishlist.urls')),
#     path('api/payments/', include('payments.urls')),
#     path('api/shipping/', include('shipping.urls')),
# ]

# # Serve media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# API Documentation URL patterns
api_docs_patterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# API endpoint URL patterns
api_patterns = [
    path('auth/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('reviews/', include('reviews.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('shipping/', include('shipping.urls')),
    path('payments/', include('payments.urls')),
    path('core/', include('core.urls')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/', include(api_docs_patterns)),

    # API Endpoints
    path('api/', include(api_patterns)),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
