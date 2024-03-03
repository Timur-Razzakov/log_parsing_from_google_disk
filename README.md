## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

## Описание проекта

Данное приложение получает ссылку с гугл диска, обрабатывает его, из ссылки просмотре делает ссылку для
скачивания, затем парсит информацию и сохраняет. Предусмотренна возможность фильтрации, как в админке так и на
странице DRF, подготовлен swagger, с описанием функционала.

## Документация к API

* Документация к API можно посмотреть тут: \
  [http://127.0.0.1:8000/api/v1/docs/swagger/](http://127.0.0.1:8000/api/v1/docs/swagger/)

## Локальный запуск

* Устанавливаем Docker
* Устанавливаем Docker compose
* Клонируем репозиторий
* Создаем файл .env в корне проекта
* Копируем в него настройки из файла .env.example

Меняем настройки для подключения к БД в файле .env:

* PG_NAME = db
* PG_USER = user
* PG_PASS = 1234
* PG_HOST = database
* PG_PORT = 5432

Для запуска прописываем:

```bash
docker compose -f docker-compose.yml up --build
```

## Локальный запуск

### Клонирование репозитория

Обратите внимание на точку в конце, это говорит о том, чтобы скопировать в текущую директорию

```bash
git clone https://github.com/Timur-Razzakov/log_parsing_from_google_disk.git .
```

### Создание БД PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE
USER name_user WITH PASSWORD 'password';
CREATE
DATABASE name_db WITH OWNER name_user;
```

### Виртуальное окружение

```bash 
python3.10 -m venv venv &&
source venv/bin/activate &&
pip install -U pip &&
pip install -r requirements.txt
```

> В Windows меняем строчку source venv/bin/activate на .\venv\Scripts\activate

### Настройки окружения

1. Создаем файл .env в корне проекта
2. Копируем в него настройки из файла .env.example
3. Прописываем в нем свои значения

## Работа с репозиторием

## Code-base structure

```bash
< PROJECT ROOT >
   |
   |-- LogsParsing/                             
   |    |-- settings.py                    
   |    |-- wsgi.py                        
   |    |-- urls.py                      
   |
   |-- apps/
   |    |
   |    |-- log_info/                          
   |    |    |-- migrations
   |    |           |-- *_init.py 
   |    |    |-- admin.py 
   |    |    |-- models.py 
   |    |    |-- apps.py 
   |    |    |-- tests.py                  
   |    |  
   |-- api/
   |    |
   |    | -- log_info/
   |    |       |-- serialyzer.py
   |    |       |-- url.py
   |    |       |-- views.py
   |-- tests
   |    | --logs_info
   |    |       | -- test_api.py
   |-- requirements.txt                     
   |-- docker-compose.yml
   |-- Dockerfile
   |-- .env                                 
   |-- manage.py                        
   |-- README.md                        
   |
   |-- ************************************************************************
```
