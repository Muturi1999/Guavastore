
from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView,
    BrandListView, BrandDetailView,
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    FeaturedProductsView, NewArrivalsView,
    BestSellersView, OnSaleProductsView,
    TagListView, SearchSuggestionsView
)

app_name = 'products'

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    
    # Brands
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail'),
    
    # Products
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    
    # Special Product Lists
    path('lists/featured/', FeaturedProductsView.as_view(), name='featured_products'),
    path('lists/new-arrivals/', NewArrivalsView.as_view(), name='new_arrivals'),
    path('lists/best-sellers/', BestSellersView.as_view(), name='best_sellers'),
    path('lists/on-sale/', OnSaleProductsView.as_view(), name='on_sale'),
    
    # Tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    
    # Search
    path('search/suggestions/', SearchSuggestionsView.as_view(), name='search_suggestions'),
]