
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView,
    UserProfileView, ChangePasswordView,
    AddressListCreateView, AddressDetailView,
    SetDefaultAddressView
)

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Addresses
    path('addresses/', AddressListCreateView.as_view(), name='address_list'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address_detail'),
    path('addresses/<int:pk>/set-default/', SetDefaultAddressView.as_view(), name='set_default_address'),
]
