from rest_framework import viewsets, permissions
from .models import Customer, Address, Wishlist, CustomerNote
from .serializers import CustomerSerializer, AddressSerializer, WishlistSerializer, CustomerNoteSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerNoteViewSet(viewsets.ModelViewSet):
    queryset = CustomerNote.objects.all()
    serializer_class = CustomerNoteSerializer
    permission_classes = [permissions.IsAdminUser]
