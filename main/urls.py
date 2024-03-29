from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product-list'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
]