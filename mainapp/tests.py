from django.test import TestCase

# Create your tests here.
import os

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from mainapp.models import Product , ShopUser


class TestMainapp(TestCase):
    def setUp(self):
        self.client = Client()
        self.super_user = ShopUser.objects.create(email='django@dj.com', user_type=2, password='django')
        self.super_user.set_password('django')
        self.super_user.save()

    def test_user_login(self):
        """
        проверяем логин пользователя
        """
        print('smoke test registered user')
        user_data = {
            'email': 'django@dj.com',
            'user_type': 2,
            'password': 'gjango',
            }

        new_user = ShopUser.objects.get(email=user_data['email'])

        print(new_user.email, new_user.password)

        # данные нового пользователя.
        self.client.force_login(user=new_user)

        # логинимся
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')

        #print(response.content.decode('utf8'))

        self.assertContains(response, text=user_data['email'], status_code=200)
        # заход в корзину
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)

        # заход в корзины
        response = self.client.get('/client-basket/')
        self.assertEqual(response.status_code, 200)

    def test_mainapp_urls(self):
        """
        Проверка страниц на открывание
        """
        print('smoke test Anonymous')
        #index
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        #products
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        #заход в корзину анонимусом
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 302)

    def test_product_create(self):
        """
        Проверка создания обьектов товаров в таблице Product
        """
        print('create product test')
        self.product_1 = Product.objects.create(article="111", name='Alpha', price_rozn=150)
        self.product_2 = Product.objects.create(article="112", name='Lambda', price_rozn=150)
        self.assertEqual(str(self.product_1), 'Alpha')
        self.assertEqual(str(self.product_2), 'Lambda')

    def tearDown(self):
        pass