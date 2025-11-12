
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product, ProductVariant
from .serializers import CartSerializer, CartItemSerializer

class CartView(APIView):
    """Get or create cart"""
    
    permission_classes = [AllowAny]
    
    def get_cart(self, request):
        """Get or create cart for user/session"""
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart
    
    def get(self, request):
        """Get cart"""
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def delete(self, request):
        """Clear cart"""
        cart = self.get_cart(request)
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemView(APIView):
    """Add, update, remove cart items"""
    
    permission_classes = [AllowAny]
    
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart
    
    def post(self, request):
        """Add item to cart"""
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        variant_id = request.data.get('variant_id')
        quantity = int(request.data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
        
        # Check if item already exists
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, pk):
        """Update cart item quantity"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, pk=pk)
        
        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_item.quantity = int(quantity)
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """Remove item from cart"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, pk=pk)
        cart_item.delete()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class ApplyCouponView(APIView):
    """Apply coupon to cart"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        from core.models import Coupon
        from django.utils import timezone
        
        code = request.data.get('code')
        
        try:
            coupon = Coupon.objects.get(code__iexact=code)
            
            if not coupon.is_valid():
                return Response({
                    'error': 'This coupon is not valid or has expired'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get cart
            if request.user.is_authenticated:
                cart, _ = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                cart, _ = Cart.objects.get_or_create(session_key=session_key)
            
            discount = coupon.calculate_discount(cart.subtotal)
            
            return Response({
                'code': coupon.code,
                'discount': discount,
                'description': coupon.description
            })
            
        except Coupon.DoesNotExist:
            return Response({
                'error': 'Invalid coupon code'
            }, status=status.HTTP_404_NOT_FOUND)