from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """Product category model"""
    
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_product_count(self):
        return self.products.filter(is_active=True).count()

class Brand(models.Model):
    """Brand model"""
    
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    """Main product model"""
    
    STOCK_STATUS_CHOICES = (
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('pre_order', 'Pre-order'),
    )
    
    # Basic Information
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, blank=True)
    
    # Categorization
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='products'
    )
    
    # Descriptions
    short_description = models.TextField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Original price before discount"
    )
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Inventory
    stock_quantity = models.IntegerField(default=0)
    stock_status = models.CharField(
        max_length=20, 
        choices=STOCK_STATUS_CHOICES, 
        default='in_stock'
    )
    low_stock_threshold = models.IntegerField(default=10)
    
    # Media
    featured_image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Status & Flags
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    
    # Stats (cached fields)
    view_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00
    )
    review_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Update stock status based on quantity
        if self.stock_quantity == 0:
            self.stock_status = 'out_of_stock'
        elif self.stock_quantity <= self.low_stock_threshold:
            self.stock_status = 'low_stock'
        else:
            self.stock_status = 'in_stock'
        
        super().save(*args, **kwargs)
    
    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

class ProductImage(models.Model):
    """Additional product images"""
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-is_featured']
    
    def __str__(self):
        return f"Image for {self.product.name}"

class ProductVariant(models.Model):
    """Product variants (color, size, etc.)"""
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='variants'
    )
    name = models.CharField(max_length=200)  # e.g., "Red - Large"
    sku = models.CharField(max_length=100, unique=True)
    
    # Variant attributes
    attributes = models.JSONField(default=dict)  # {"color": "Red", "size": "Large"}
    
    # Pricing (can override main product price)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Stock
    stock_quantity = models.IntegerField(default=0)
    
    # Media
    image = models.ImageField(upload_to='variants/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    @property
    def final_price(self):
        return self.price if self.price else self.product.price

class Tag(models.Model):
    """Product tags"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    products = models.ManyToManyField(Product, related_name='tags', blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)