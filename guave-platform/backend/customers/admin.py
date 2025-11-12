# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Customer, Address, Wishlist, CustomerNote

# @admin.register(Customer)
# class CustomerAdmin(UserAdmin):
#     model = Customer
#     list_display = ('email', 'first_name', 'last_name', 'customer_type', 'is_active', 'is_staff', 'total_orders', 'loyalty_points', 'created_at')
#     list_filter = ('customer_type', 'is_active', 'is_staff', 'email_marketing')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('-created_at',)
#     readonly_fields = ('created_at', 'updated_at', 'last_login_at')

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'customer_type')}),
#         ('Preferences', {'fields': ('email_marketing', 'email_orders', 'email_promotions')}),
#         ('Stats', {'fields': ('total_orders', 'total_spent', 'average_order_value', 'loyalty_points')}),
#         ('Important dates', {'fields': ('last_login_at', 'created_at', 'updated_at')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#     )

# @admin.register(Address)
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'customer', 'city', 'country', 'is_default_shipping', 'is_default_billing', 'created_at')
#     list_filter = ('country', 'is_default_shipping', 'is_default_billing')
#     search_fields = ('full_name', 'city', 'customer__email')

# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'product', 'created_at')
#     search_fields = ('customer__email', 'product__name')

# @admin.register(CustomerNote)
# class CustomerNoteAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'created_by', 'is_internal', 'created_at')
#     search_fields = ('customer__email', 'note')
#     list_filter = ('is_internal',)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Address, Wishlist, CustomerNote

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'customer_type', 'total_orders', 'total_spent', 'is_active']
    list_filter = ['customer_type', 'is_active', 'email_marketing']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'date_of_birth')}),
        ('Customer Type', {'fields': ('customer_type',)}),
        ('Email Preferences', {'fields': ('email_marketing', 'email_orders', 'email_promotions')}),
        ('Stats', {'fields': ('total_orders', 'total_spent', 'average_order_value', 'loyalty_points')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    
    readonly_fields = ['total_orders', 'total_spent', 'average_order_value']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'full_name', 'city', 'country', 'address_type', 'is_default_shipping']
    list_filter = ['address_type', 'country', 'is_default_shipping', 'is_default_billing']
    search_fields = ['full_name', 'city', 'postal_code', 'customer__email']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__email', 'product__name']

@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_by', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['customer__email', 'note']