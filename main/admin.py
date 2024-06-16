from django.contrib import admin
from .models import Product, Category, ProductImage, GalleryImage, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['description', 'image']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'postal_code', 'city', 'country', 'created_at', 'updated_at', 'total_price', 'status']
    list_filter = ['created_at', 'updated_at', 'status']
    inlines = [OrderItemInline]