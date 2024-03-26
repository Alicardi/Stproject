from django.shortcuts import render
from .models import Product, Category

def index(request):
    return render(request, 'main/index.html')

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)

    # Сортировка
    sort_by = request.GET.get('sort_by')
    if sort_by:
        products = products.order_by(sort_by)

    return render(request, 'main/product_list.html', {'products': products, 'categories': categories})
