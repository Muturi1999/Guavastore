from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, related_name='orders')
    
    # Customer details (saved for record)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Shipping address
    shipping_full_name = models.CharField(max_length=200)
    shipping_address_line1 = models.CharField(max_length=300)
    shipping_address_line2 = models.CharField(max_length=300, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    
    # Billing address
    billing_full_name = models.CharField(max_length=200)
    billing_address_line1 = models.CharField(max_length=300)
    billing_address_line2 = models.CharField(max_length=300, blank=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=20)
    billing_country = models.CharField(max_length=100)
    
    # Order totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Payment
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=200, blank=True)
    
    # Shipping
    shipping_method = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=200, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Coupon
    coupon_code = models.CharField(max_length=50, blank=True)
    
    # Notes
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-XXXXX
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f'ORD-{date_str}').order_by('-order_number').first()
            
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.order_number = f'ORD-{date_str}-{new_number:05d}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Product details (saved for record)
    product_name = models.CharField(max_length=300)
    product_sku = models.CharField(max_length=100)
    variant_details = models.JSONField(null=True, blank=True)
    
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class OrderStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order Status Histories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"


class ShippingMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_days_min = models.IntegerField(validators=[MinValueValidator(1)])
    estimated_days_max = models.IntegerField(validators=[MinValueValidator(1)])
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} - {self.estimated_days_min}-{self.estimated_days_max} days"