import django_filters
from .models import Product, Category, Brand

class ProductFilter(django_filters.FilterSet):
    """Advanced product filtering"""
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all())
    in_stock = django_filters.BooleanFilter(field_name='stock_quantity', lookup_expr='gt', label='In Stock')
    
    class Meta:
        model = Product
        fields = ['category', 'brand', 'is_featured', 'is_new', 'is_on_sale']