# from django.contrib import admin
# from .models import Wishlist, WishlistItem

# class WishlistItemInline(admin.TabularInline):
#     model = WishlistItem
#     extra = 0

# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ['user', 'item_count', 'updated_at']
#     search_fields = ['user__email']
#     readonly_fields = ['item_count', 'created_at', 'updated_at']
#     inlines = [WishlistItemInline]