from django.contrib import admin
from .models import Product, Category, ProductImage, GalleryImage

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['description', 'image']