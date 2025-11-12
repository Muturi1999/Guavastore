from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant
from accounts.models import Address
from decimal import Decimal

class Order(models.Model):
    """Order model"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    # Order Info
    order_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    # Customer Info
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Addresses
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='shipping_orders'
    )
    billing_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='billing_orders',
        null=True,
        blank=True
    )
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, blank=True)
    
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
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Order item model"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    
    # Product snapshot (in case product changes)
    product_name = models.CharField(max_length=500)
    product_sku = models.CharField(max_length=100)
    variant_name = models.CharField(max_length=200, blank=True)
    
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
    
    def save(self, *args, **kwargs):
        # Calculate subtotal
        self.subtotal = self.price * self.quantity
        
        # Save product snapshot
        self.product_name = self.product.name
        self.product_sku = self.product.sku
        if self.variant:
            self.variant_name = self.variant.name
        
        super().save(*args, **kwargs)

class OrderStatusHistory(models.Model):
    """Track order status changes"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Order status histories'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.status}"
