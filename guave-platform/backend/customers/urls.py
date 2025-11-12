from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AddressViewSet, WishlistViewSet, CustomerNoteViewSet

router = DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('addresses', AddressViewSet)
router.register('wishlists', WishlistViewSet)
router.register('notes', CustomerNoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
