from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Brand, Product
from .serializers import (CategorySerializer, BrandSerializer, 
                          ProductListSerializer, ProductDetailSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images', 'variants', 'specifications')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'stock_status', 'is_featured', 'is_new']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['created_at', 'price', 'name', 'views_count', 'sales_count']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.queryset.filter(is_featured=True)[:12]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        new_products = self.queryset.filter(is_new=True).order_by('-created_at')[:12]
        serializer = self.get_serializer(new_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def best_selling(self, request):
        best_selling = self.queryset.order_by('-sales_count')[:12]
        serializer = self.get_serializer(best_selling, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        on_sale = self.queryset.filter(compare_price__isnull=False, compare_price__gt=models.F('price'))[:12]
        serializer = self.get_serializer(on_sale, many=True)
        return Response(serializer.data)