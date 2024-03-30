from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import logout_view

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product-list'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
   path('logout/', logout_view, name='logout'),
]