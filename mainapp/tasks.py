import os
import subprocess
import tempfile

from celery import shared_task
from time import sleep

from start_mag import settings
from mainapp.models import ShopUser

from django.template.loader import render_to_string

#dummy async function with one param
@shared_task
def sleepy(duration):
    sleep(duration)
    print('sleep is over!')
    return None

#async pdf processing function
#celery -A start_mag worker -l info
#pk is user_id
# поля (по одному на строку): Клиент, Номер заказа, Адрес доставки.
# т.к. заказа нет то номер заказа от болды, клиент - сам пользователь.
@shared_task
def async_pdf_process(pk):
    print(f'received async call to form manifest for user {pk}')

    user_qs = ShopUser.objects.filter(id=pk).values('email','addr_dost')

    context = {
        'client_name': user_qs[0]['email'],
        'order_no': '12345678',
        'address': user_qs[0]['addr_dost'],
    }
    manifest = render_to_string('manifest.txt', context)
    with tempfile.NamedTemporaryFile(suffix='.html', dir=os.path.dirname(__file__), delete=False,
                                     mode='w', encoding='utf-8') as temp_html:
        temp_html.write(manifest)

    with tempfile.NamedTemporaryFile(suffix='.pdf', dir=settings.PDF_PATH, delete=False) as temp_pdf:
        pass
    # Run wkhtmltopdf via the appropriate subprocess call
    wkhtmltopdfargs = f'{settings.PDF_BIN} {temp_html.name} {temp_pdf.name}'

    try:
        subprocess.check_output(wkhtmltopdfargs, shell=True)
    except:
        pass
    # Remove the temporary files created
    os.remove(temp_html.name)

    print(f'finished - pdf saved. {temp_pdf.name}')

    return None