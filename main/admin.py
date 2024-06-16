from django.contrib import admin
from .models import Product, Category, ProductImage, GalleryImage, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['description', 'image']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')