from django.core.management.base import BaseCommand
from mainapp.models import Product, ShopUser

import json, os, csv

CSV_PATH = 'mainapp/csv'


def load_from_csv(file_name):
    with open(os.path.join(CSV_PATH, file_name), 'r') as infile:
        F_N_READER = csv.reader(infile, delimiter=';')
        return list(F_N_READER)


# Сопоставление полей:
# - Артикул = "ПТ"+"КодТовараПоставщика"
# - Наименование товара = "НаименованиеТовараПоставщика"
# - Цена закуп = 0.9 * "ЦенаПоставщика"
# - Цена розница = если "ЦенаПоставщика" < 1000 руб, то 1.2 * "ЦенаПоставщика". иначе 1.1 * "ЦенаПоставщика"
class Command(BaseCommand):
    def handle(self, *args, **options):

        goods = load_from_csv('goods.csv')

        goods.pop(0)

        Product.objects.all().delete()

        for item in goods:
            print(item)
            if int(item[2]) < 1000:
                price_rozn = 1.2 * int(item[2])
            else:
                price_rozn = 1.1 * int(item[2])

            product = {
                'article': 'ПТ' + item[0],
                'name': item[1],
                'price_rozn': price_rozn,
                'price_zakup': 0.9 * int(item[2]),
            }

            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя/манагера при помощи менеджера модели
        super_user = ShopUser.objects.create_superuser('django@dj.com', 2, 'django')

        print('goods added, superuser/manager created! login: django@dj.com password: django')
