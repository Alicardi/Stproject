from django.shortcuts import render
from .models import Product, Category, GalleryImage
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from .forms import SignUpForm


def index(request):
    images = GalleryImage.objects.all()
    return render(request, 'main/index.html', {'images': images})

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

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Автоматически войти после регистрации
            return redirect('index')  # Перенаправить на главную страницу
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')