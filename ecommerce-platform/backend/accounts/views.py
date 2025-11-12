from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, UserSerializer, UserUpdateSerializer,
    ChangePasswordSerializer, AddressSerializer
)
from .models import Address

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    """User login endpoint"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = User.objects.get(email=request.data.get('email'))
            response.data['user'] = UserSerializer(user).data
        
        return response

class LogoutView(APIView):
    """User logout endpoint"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response(serializer.data)

class ChangePasswordView(APIView):
    """Change user password"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AddressListCreateView(generics.ListCreateAPIView):
    """List and create addresses"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete address"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

class SetDefaultAddressView(APIView):
    """Set address as default"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
            address.is_default = True
            address.save()
            
            return Response({
                'message': 'Default address updated',
                'address': AddressSerializer(address).data
            }, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({
                'error': 'Address not found'
            }, status=status.HTTP_404_NOT_FOUND)