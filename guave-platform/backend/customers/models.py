from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    CUSTOMER_TYPE_CHOICES = [
        ('new', 'New Customer'),
        ('returning', 'Returning Customer'),
        ('vip', 'VIP Customer'),
        ('inactive', 'Inactive Customer'),
    ]

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='new')
    
    # Email preferences
    email_marketing = models.BooleanField(default=True)
    email_orders = models.BooleanField(default=True)
    email_promotions = models.BooleanField(default=True)
    
    # Customer stats
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Loyalty points
    loyalty_points = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email} - {self.get_full_name()}"

    class Meta:
        ordering = ['-created_at']


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=300)
    address_line2 = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Kenya')
    
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='home')
    
    is_default_shipping = models.BooleanField(default=False)
    is_default_billing = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['-is_default_shipping', '-created_at']

    def save(self, *args, **kwargs):
        if self.is_default_shipping:
            Address.objects.filter(customer=self.customer, is_default_shipping=True).update(is_default_shipping=False)
        if self.is_default_billing:
            Address.objects.filter(customer=self.customer, is_default_billing=True).update(is_default_billing=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.address_line1}, {self.city}"


class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['customer', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.email} - {self.product.name}"


class CustomerNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='notes_created')
    is_internal = models.BooleanField(default=True, help_text='Only visible to staff')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.customer.email} - {self.created_at.strftime('%Y-%m-%d')}"