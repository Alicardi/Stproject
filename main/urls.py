from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product-list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]