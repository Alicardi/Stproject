from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) # Использовать как бренд
    name = models.CharField(max_length=100)

    volume = models.CharField(max_length=100, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    secondary_image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    
class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_images/')
    description = models.CharField(max_length=255, blank=True)

def __str__(self):
    return f"Image {self.id} - {self.description[:20]}"
    
