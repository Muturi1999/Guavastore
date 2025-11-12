from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.core.cache import cache
from .models import Category, Brand, Product, Tag
from .serializers import (
    CategorySerializer, BrandSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer, TagSerializer
)
from .filters import ProductFilter

class CategoryListView(generics.ListAPIView):
    """List all categories"""
    
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        # Cache categories for 1 hour
        cache_key = 'all_categories'
        categories = cache.get(cache_key)
        
        if categories is None:
            categories = Category.objects.filter(
                is_active=True,
                parent__isnull=True
            ).prefetch_related('children')
            cache.set(cache_key, categories, 3600)
        
        return categories

class CategoryDetailView(generics.RetrieveAPIView):
    """Get category details"""
    
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)

class BrandListView(generics.ListAPIView):
    """List all brands"""
    
    serializer_class = BrandSerializer
    
    def get_queryset(self):
        queryset = Brand.objects.filter(is_active=True)
        
        # Add product count
        queryset = queryset.annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        )
        
        # Filter featured brands if requested
        if self.request.query_params.get('featured') == 'true':
            queryset = queryset.filter(featured=True)
        
        return queryset

class BrandDetailView(generics.RetrieveAPIView):
    """Get brand details"""
    
    serializer_class = BrandSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Brand.objects.filter(is_active=True)

class ProductListView(generics.ListAPIView):
    """List products with filtering, search, and sorting"""
    
    serializer_class = ProductListSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'short_description', 'sku']
    ordering_fields = [
        'created_at', 'price', 'average_rating',
        'sold_count', 'view_count', 'name'
    ]
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        )
        
        # Special filters
        if self.request.query_params.get('featured') == 'true':
            queryset = queryset.filter(is_featured=True)
        
        if self.request.query_params.get('on_sale') == 'true':
            queryset = queryset.filter(is_on_sale=True)
        
        if self.request.query_params.get('new') == 'true':
            queryset = queryset.filter(is_new=True)
        
        # Category filter
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(
                Q(category__slug=category_slug) |
                Q(category__parent__slug=category_slug)
            )
        
        # Brand filter
        brand_slug = self.request.query_params.get('brand')
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        
        # Price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Rating filter
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
        
        # In stock filter
        if self.request.query_params.get('in_stock') == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)
        
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    """Get product details"""
    
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related(
            'images', 'variants', 'tags'
        )

class ProductCreateView(generics.CreateAPIView):
    """Create new product (admin only)"""
    
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductUpdateView(generics.UpdateAPIView):
    """Update product (admin only)"""
    
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ProductDeleteView(generics.DestroyAPIView):
    """Delete product (admin only)"""
    
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class FeaturedProductsView(generics.ListAPIView):
    """Get featured products"""
    
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        cache_key = 'featured_products'
        products = cache.get(cache_key)
        
        if products is None:
            products = Product.objects.filter(
                is_active=True,
                is_featured=True
            ).select_related('category', 'brand')[:12]
            cache.set(cache_key, products, 1800)  # 30 minutes
        
        return products

class NewArrivalsView(generics.ListAPIView):
    """Get new arrival products"""
    
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
            is_new=True
        ).select_related('category', 'brand').order_by('-created_at')[:12]

class BestSellersView(generics.ListAPIView):
    """Get best selling products"""
    
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).select_related('category', 'brand').order_by('-sold_count')[:12]

class OnSaleProductsView(generics.ListAPIView):
    """Get products on sale"""
    
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
            is_on_sale=True
        ).select_related('category', 'brand')[:12]

class TagListView(generics.ListAPIView):
    """List all tags"""
    
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

class SearchSuggestionsView(APIView):
    """Get search suggestions"""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if len(query) < 2:
            return Response([])
        
        # Search products
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(sku__icontains=query),
            is_active=True
        )[:5]
        
        # Search categories
        categories = Category.objects.filter(
            name__icontains=query,
            is_active=True
        )[:3]
        
        # Search brands
        brands = Brand.objects.filter(
            name__icontains=query,
            is_active=True
        )[:3]
        
        return Response({
            'products': ProductListSerializer(products, many=True).data,
            'categories': CategorySerializer(categories, many=True).data,
            'brands': BrandSerializer(brands, many=True).data,
        })