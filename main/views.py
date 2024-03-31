from django.shortcuts import render
from .models import Product, Category, GalleryImage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages



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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неправильный логин или пароль')
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        # Получение данных из POST запроса
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')
        
        # Проверка данных
        if password != password_confirm:
            return render(request, 'main/base.html', {'error': 'Пароли не совпадают'})
        
        # Создание пользователя
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)  # Автоматический вход пользователя
            return redirect('home')
        except Exception as e:
            return render(request, 'main/base.html', {'error': str(e)})
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    # Убедитесь, что пользователь авторизован
    if not request.user.is_authenticated:
        return redirect('username')
    # Ваш код для обработки данных пользователя
    # ...
    return render(request, 'main/profile.html')