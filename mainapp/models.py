from django.db import models

# Create your models here.
# Модели (типы полей выбрать из представляемых фреймворком):
# - Учетные записи пользователей: ФИО, адрес доставки, email (он же логин), пароль, роль.
# - Роли пользователей: клиент, менеджер.
# - Товары: артикул (текст), наименование, цена закуп, цена розница.
# - Корзина: клиент, товар, количество, цена, сумма по строке.

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.conf import settings

class ShopUserManager(BaseUserManager):
    """
    User manager
    """
    def create_user(self, email, user_type, password=None):
        """
        Creates and saves a User with the given email, user_type and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, user_type, password):
        """
        Creates and saves a superuser with the given email, user_type and password.
        """
        user = self.create_user(email,
                                password=password,
                                user_type=user_type,
                                )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class ShopUser(AbstractUser):
    """
    Своя модель пользователя
    """
    USER_TYPE_CHOICES = (
        (1, 'Клиент'),
        (2, 'Манагер'),
    )
    username = None
    email = models.CharField(max_length=200, unique=True)
    fio = models.CharField(max_length=100, blank=True)
    addr_dost = models.CharField(max_length=200, blank=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    objects = ShopUserManager()


class Product(models.Model):
    """
    Таблица товаров
    """
    article = models.CharField(verbose_name='артикул', max_length=100)
    name = models.CharField(verbose_name='наименование', max_length=100)
    price_zakup = models.DecimalField(verbose_name='цена продукта закупочная', max_digits=8, decimal_places=2, default=0)
    price_rozn = models.DecimalField(verbose_name='цена продукта розничная', max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name



class Basket(models.Model):
    """
    Корзина
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    #price = models.PositiveIntegerField(verbose_name='цена', default=0)

    @property
    def sum_price(self):
        return self.product.price_rozn * self.quantity

    @property
    def get_quantity(self):
        return self.quantity
