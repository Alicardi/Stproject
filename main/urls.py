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
    path('add_to_cart/<int:productId>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
]