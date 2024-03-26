from django.shortcuts import render
from .models import Product

def index(request):
    return render(request, 'main/index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product_list.html', {'products': products})