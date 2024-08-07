from django.urls import path
from . import views
from .views import logout_view, change_password, add_to_cart

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product-list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('verify-email/<slug:user_id>/<slug:token>/', views.verify_email, name='verify-email'),
    path('change_password/', change_password, name='change_password'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('change_quantity/<int:product_id>/', views.change_quantity, name='change_quantity'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_checkout/', views.process_checkout, name='process_checkout'),
    path('api/book_appointment/', views.book_appointment, name='book_appointment'),
]