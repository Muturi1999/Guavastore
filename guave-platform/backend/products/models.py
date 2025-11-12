from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='categories/banners/', null=True, blank=True)
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('pre_order', 'Pre-order'),
        ('coming_soon', 'Coming Soon'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    short_description = models.TextField(max_length=500)
    description = models.TextField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    stock_quantity = models.IntegerField(default=0)
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')
    low_stock_threshold = models.IntegerField(default=10)
    
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Weight in kg')
    dimensions = models.CharField(max_length=100, blank=True, help_text='L x W x H in cm')
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)
    
    views_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

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
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'created_at']

    def save(self, *args, **kwargs):
        if self.is_main:
            # Set all other images of this product to not main
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Image {self.display_order}"


class ProductAttribute(models.Model):
    ATTRIBUTE_TYPE_CHOICES = [
        ('color', 'Color'),
        ('size', 'Size'),
        ('storage', 'Storage'),
        ('memory', 'Memory'),
        ('material', 'Material'),
        ('custom', 'Custom'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    attribute_type = models.CharField(max_length=20, choices=ATTRIBUTE_TYPE_CHOICES)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_attribute_type_display()})"


class ProductAttributeValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)
    color_code = models.CharField(max_length=7, blank=True, help_text='Hex color code for color attributes')
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'value']
        unique_together = ['attribute', 'value']

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    attributes = models.ManyToManyField(ProductAttributeValue)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='variants/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        attrs = ', '.join([f"{av.attribute.name}: {av.value}" for av in self.attributes.all()])
        return f"{self.product.name} - {attrs}"


class ProductSpecification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"


class ProductBadge(models.Model):
    BADGE_TYPE_CHOICES = [
        ('new', 'New'),
        ('hot', 'Hot'),
        ('sale', 'Sale'),
        ('featured', 'Featured'),
        ('limited', 'Limited Edition'),
        ('custom', 'Custom'),
    ]

    POSITION_CHOICES = [
        ('top-left', 'Top Left'),
        ('top-right', 'Top Right'),
        ('bottom-left', 'Bottom Left'),
        ('bottom-right', 'Bottom Right'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPE_CHOICES)
    text = models.CharField(max_length=50)
    background_color = models.CharField(max_length=7, default='#FF0000')
    text_color = models.CharField(max_length=7, default='#FFFFFF')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='top-left')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductBadgeAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='badge_assignments')
    badge = models.ForeignKey(ProductBadge, on_delete=models.CASCADE)
    auto_assigned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'badge']

    def __str__(self):
        return f"{self.product.name} - {self.badge.name}"