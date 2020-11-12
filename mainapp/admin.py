from django.contrib import admin

# Register your models here.

# - управление учетками и товарами - через Django админку.
from .models import ShopUser , Product
admin.site.register(ShopUser)
admin.site.register(Product)