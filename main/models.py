from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/products/')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/products/')

    def __str__(self):
        return f"Image for {self.product.name}"
    
class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_images/')
    description = models.CharField(max_length=255, blank=True)

def __str__(self):
    return f"Image {self.id} - {self.description[:20]}"
    
