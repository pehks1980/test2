"""start_mag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from mainapp.views import UserLoginView, UserLogoutView, ProductsView, BasketView, main, basket_add, basket_del, ClientBasketView, export_pdf

urlpatterns = [
    path('', main, name='main'),
    #встроенная админка
    path('admin/', admin.site.urls),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    #управление корзиной
    path('add/<int:pk>/', basket_add, name='add'),
    path('del/<int:pk>/', basket_del, name='del'),
    #экспорт накладной в pdf
    path('pdf/', export_pdf, name='pdf'),
    #просмотр корзины пользователем
    path('basket/', BasketView.as_view(), name='basket'),
    #просмотр корзины пользователей
    path('client-basket/', ClientBasketView.as_view(), name='client_basket'),
    #просмотр товаров
    path('products/', ProductsView.as_view(), name='products'),
]
