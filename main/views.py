from .models import Product, Category, GalleryImage, Cart, CartItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


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
            return JsonResponse({'success': True})
        elif user is not None and not user.is_email_verified:
            return JsonResponse({'success': False, 'error': 'Пожалуйста, подтвердите ваш email перед входом.'})
        else:
            return JsonResponse({'success': False, 'error': 'Неправильный логин или пароль'})
    return JsonResponse({'success': False, 'error': 'Только POST запросы поддерживаются'}, status=405)


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')
        
        if password != password_confirm:
            return JsonResponse({'success': False, 'error': 'Пароли не совпадают'})
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Имя пользователя уже занято'})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Этот адрес электронной почты уже используется'})
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'Некорректный адрес электронной почты'})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False  # Не активируем пользователя сразу
            user.save()

            # Создаем токен для верификации и отправляем email
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            send_mail(
                'Подтвердите вашу учетную запись',
                f"Пожалуйста, перейдите по ссылке ниже для подтверждения вашей учетной записи: http://{request.get_host()}/verify-email/{uidb64}/{token}/",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'Пожалуйста, проверьте ваш email для завершения регистрации.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Только POST запросы поддерживаются'}, status=405)

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('username')
    return render(request, 'main/profile.html')

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    subject = 'Подтверждение электронной почты'
    message = f"Для подтверждения электронной почты перейдите по ссылке: http://{request.get_host()}/verify-email/{user.pk}/{token}/"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
def verify_email(request, user_id, token):
    try:
        # Декодируем идентификатор пользователя из base64
        uid = force_str(urlsafe_base64_decode(user_id))
        # Используем декодированный UID для получения объекта User
        user = get_object_or_404(User, pk=uid)

        # Проверяем, верный ли токен и если да, то активируем пользователя
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()  
            return redirect('home')
        else:
            # Если токен не верный, возвращаем ошибку
            return JsonResponse({'success': False, 'error': 'Ссылка недействительна или устарела'})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # В случае исключения возвращаем ошибку
        return JsonResponse({'success': False, 'error': 'Недопустимый запрос'})
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Обновляем сессию, чтобы не выходить из системы
            # Перенаправляем на страницу успешного изменения пароля или выводим сообщение
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def add_to_cart(request, productId):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=productId)
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
        # Предоставление данных о продукте в ответе
        return JsonResponse({
            'success': True,
            'product_name': product.name,
            'product_price': product.price,
            'product_image': product.image.url
        })
    else:
        return JsonResponse({'success': False, 'message': 'Пользователь не аутентифицирован'}, status=401)

def cart_view(request):
    # здесь логика для обработки данных корзины, например:
    cart_items = request.session.get('cart', [])
    total_price = sum(item['quantity'] * item['price'] for item in cart_items)
    return render(request, 'main/cart.html', {'cart': cart_items, 'total_price': total_price})