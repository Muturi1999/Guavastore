import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guava_backend.settings')
django.setup()

from products.models import Category, Brand, Product, ProductImage
from decimal import Decimal

# Create categories
electronics = Category.objects.create(name='Electronics', description='Electronic devices and accessories')
smartphones = Category.objects.create(name='Smartphones', parent=electronics, description='Mobile phones and accessories')
laptops = Category.objects.create(name='Laptops', parent=electronics, description='Laptop computers')
headphones = Category.objects.create(name='Headphones', parent=electronics, description='Audio equipment')

# Create brands
apple = Brand.objects.create(name='Apple', is_featured=True)
samsung = Brand.objects.create(name='Samsung', is_featured=True)
lenovo = Brand.objects.create(name='Lenovo')
hp = Brand.objects.create(name='HP')

# Create sample products
product1 = Product.objects.create(
    name='iPhone 15 Pro Max 256GB',
    sku='IPHON-15PM-256',
    category=smartphones,
    brand=apple,
    short_description='Latest iPhone with Pro camera system',
    description='The iPhone 15 Pro Max features the powerful A17 Pro chip, titanium design, and advanced camera system.',
    price=Decimal('1299.99'),
    compare_price=Decimal('1499.99'),
    stock_quantity=50,
    is_featured=True,
    is_new=True
)

product2 = Product.objects.create(
    name='Samsung Galaxy S24 Ultra 512GB',
    sku='SAM-S24U-512',
    category=smartphones,
    brand=samsung,
    short_description='Premium Android flagship with S Pen',
    description='Galaxy S24 Ultra with 200MP camera, built-in S Pen, and Galaxy AI features.',
    price=Decimal('1199.99'),
    compare_price=Decimal('1399.99'),
    stock_quantity=35,
    is_featured=True
)

product3 = Product.objects.create(
    name='Lenovo ThinkPad X1 Carbon Gen 11',
    sku='LEN-X1C-G11',
    category=laptops,
    brand=lenovo,
    short_description='Ultra-portable business laptop',
    description='14-inch business laptop with Intel Core i7, 16GB RAM, 512GB SSD.',
    price=Decimal('1599.99'),
    stock_quantity=20,
    is_featured=True
)

print("Sample data loaded successfully!")
