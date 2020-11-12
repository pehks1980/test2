# start_mag

Тестовое задание для вакансии СТАРТЕКС.

## Installation

1 Клонирование репозитория.

    mkdir start_mag
    
    git clone https://github.com/pehks1980/test2.git start_mag

2 Установка виртуальной среды.

    cd start_mag
    mkdir env
    virtualenv -p python3 env
    . env/bin/activate

3 Установка пакетов для работы ПО.
    
     pip install -r requirements.txt

    
4 Установка wkhtmltopdf

     sudo apt install wget xfonts-75dpi
     cd /tmp
     wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
     sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
     which wkhtmltopdf
     
     путь поставить в настройку start_mag/settings.py:
     PDF_BIN = '/usr/local/bin/wkhtmltopdf'
     
    
4 Миграции.

    python manage.py makemigrations mainapp
    
    python manage.py migrate
    
5 Настройка celery сервера брокера (rabbitmq)

    Если есть docker - самый простой метод 1 команда:
    
    docker run -d -p 5672:5672 rabbitmq
    
    Иначе необходимо изменить настройку сервера брокера в start_mag/settings.py
    
    CELERY_BROKER_URL='pyamqp://guest@localhost/'


## Run (in testing mode)

    (в отдельной консоли) celery -A start_mag worker -l info
    
    python manage.py runserver

    open browser and put http://127.0.0.1:8000 to open index page
    
    pdf файл накладной сохраняется в папке:
    staticfiles/pdf (имя выбирается сл.набором символов)


## Test (smoketest)
    
    python manage.py test 
    

## e-mail: pehks1980@gmail.com

## github: http://github.com/pehks1980
