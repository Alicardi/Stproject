from .models import Product, Category, GalleryImage, Cart, CartItem, Order, OrderItem, Appointment
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
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import CheckoutForm
from django.views.decorators.csrf import csrf_exempt
import json
# from .cart import Cart
from decimal import Decimal
import logging
logger = logging.getLogger(__name__)


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
        return redirect('login')  # Перенаправление на страницу входа, если пользователь не авторизован

    # Загрузка истории заказов пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Загрузка записей пользователя
    appointments = Appointment.objects.filter(user=request.user).order_by('-date', '-time')  # Предполагаем, что есть поля date и time

    return render(request, 'main/profile.html', {'orders': orders, 'appointments': appointments})

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

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    quantity = request.POST.get('quantity', 1)
    cart.add(product=product, quantity=int(quantity), update_quantity=False)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'product_id': product_id, 'product_name': product.name, 'quantity': quantity})
    else:
        return redirect('cart')
    
@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart')

    
def cart_view(request):
    cart = Cart(request)
    cart_items = cart.get_items()  # Пример функции, возвращающей элементы корзины как список словарей
    total_price = sum(item['quantity'] * item['price'] for item in cart_items)
    return render(request, 'main/cart.html', {'cart': cart_items, 'total_price': total_price})

@require_POST
def change_quantity(request, product_id):
    delta = int(request.POST.get('delta', 0))
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    new_quantity = cart.update_quantity(product, delta)
    if new_quantity <= 0:
        cart.remove(product)
        new_quantity = 0
    total_price = cart.get_total_price()

    return JsonResponse({
        'success': True,
        'new_quantity': new_quantity,
        'product_price': f"{product.price:.2f}",
        'total_price': f"{total_price:.2f}"
    })

class Cart:
    def __init__(self, request):
        """
        Инициализация корзины. Пытаемся получить корзину из текущей сессии.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавление товара в корзину или обновление его количества.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def update_quantity(self, product, delta):
        """Обновление количества заданного продукта."""
        product_id = str(product.id)
        if product_id in self.cart:
            # Увеличиваем или уменьшаем количество товара
            self.cart[product_id]['quantity'] += delta
            # Проверяем, не упало ли количество ниже нуля
            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product)  # Если да, удаляем товар из корзины
                return 0
            self.save()  # Сохраняем изменения в сессии
            return self.cart[product_id]['quantity']
        else:
            # Если продукт не найден в корзине, возможно стоит добавить его
            self.add(product, quantity=delta)
            self.save()
            return self.cart[product_id]['quantity'] if product_id in self.cart else 0

    def save(self):
        # обновляем сессию cart
        self.session['cart'] = self.cart
        # отметить сессию как "измененную", чтобы убедиться, что она сохранена
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет всех товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_items(self):
        items = []
        for item_id, item_data in self.cart.items():
            product = Product.objects.get(id=item_id)
            items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': product.price
            })
        return items

def checkout(request):
    form = CheckoutForm()  # Создайте экземпляр формы
    return render(request, 'main/checkout.html', {'form': form})

def process_checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Создание заказа из данных формы
            order = Order(
                user=request.user,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country']
            )
            order.save()
            
            # Перенос товаров из корзины в заказ
            cart = Cart(request)
            total_price = 0
            for item_id, item_data in cart.cart.items():
                product = Product.objects.get(id=item_id)
                order_item = OrderItem(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item_data['quantity']
                )
                order_item.save()
                total_price += product.price * item_data['quantity']
            
            # Обновление общей цены заказа
            order.total_price = total_price
            order.save()

            # Очистка корзины
            cart.clear()
            
            return redirect('profile')
        else:
            # Если форма невалидна, возвращаемся на страницу оформления заказа с ошибками
            return render(request, 'main/checkout.html', {'form': form})
    else:
        # Если это не POST запрос, то инициализируем пустую форму
        form = CheckoutForm()

    return render(request, 'main/checkout.html', {'form': form})

@csrf_exempt
def book_appointment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        date = data.get('date')
        time = data.get('time')
        user = request.user
        
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не авторизован'}, status=401)
        
        if date and time:
            appointment = Appointment.objects.create(
                user=user,
                date=date,
                time=time,
                service='Сеанс загара'  # Или любая другая услуга по умолчанию
            )
            return JsonResponse({'success': 'Услуга успешно забронирована'})
        else:
            return JsonResponse({'error': 'Неверные время или дата'}, status=400)
    
    return JsonResponse({'error': 'Неверный метод запроса'}, status=405)
