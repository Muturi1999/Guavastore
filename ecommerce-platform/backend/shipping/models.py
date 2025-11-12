from django.db import models
from django.conf import settings
from datetime import timedelta, date

class ShippingMethod(models.Model):
    """Available shipping methods."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_days_min = models.IntegerField(default=3)
    estimated_days_max = models.IntegerField(default=7)
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['cost']

    def __str__(self):
        return f"{self.name} (${self.cost})"

    def get_cost(self, order_total):
        """Returns calculated cost (0 if above free shipping threshold)."""
        if self.free_shipping_threshold and order_total >= self.free_shipping_threshold:
            return 0
        return self.cost

    def get_estimated_delivery_window(self):
        """Returns min and max delivery date estimates."""
        today = date.today()
        return {
            'min': today + timedelta(days=self.estimated_days_min),
            'max': today + timedelta(days=self.estimated_days_max),
        }


class ShippingAddress(models.Model):
    """Customer shipping address."""
    ADDRESS_TYPES = (
        ('home', 'Home'),
        ('office', 'Office'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    county_or_state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES)
    is_default = models.BooleanField(default=False)
    use_as_billing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"


class OrderShipping(models.Model):
    """Links an order with chosen shipping method and address."""
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='shipping')
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_delivery = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Shipping for Order #{self.order.id}"


class OrderTracking(models.Model):
    """Track shipping progress."""
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('delayed', 'Delayed'),
    )

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='tracking')
    tracking_number = models.CharField(max_length=100, unique=True)
    carrier = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    current_location = models.CharField(max_length=255, blank=True, null=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking #{self.tracking_number} ({self.status})"


class TrackingEvent(models.Model):
    """Detailed timeline for tracking updates."""
    tracking = models.ForeignKey(OrderTracking, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} - {self.location}"
