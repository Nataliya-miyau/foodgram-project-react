[![foodgram-project-react workflow](https://github.com/Nataliya-miyau/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/Nataliya-miyau/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

Проект доступен по адресу http://foodgram.ravenous.space/signin

# «Продуктовый помощник» Foodgram

## Описание проекта

Foodgram - это приложение, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Стек технологий

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

## Установка проекта локально
+ Склонировать репозиторий на локальную машину:
```
git clone git@github.com:Nataliya-miyau/foodgram-project-react.git
cd foodgram-project-react
```
+ Cоздать и активировать виртуальное окружение:
```
python3.9 -m venv venv
source venv/bin/activate
```
+ Cоздать файл .env в директории /infra/ с содержанием:
```
SECRET_KEY=секретный ключ django
ALLOWED_HOSTS='ip localhost'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
+ Перейти в директирию backend и установить зависимости:
```
cd backend/
pip install -r requirements.txt
```
+ Выполнить миграции и запустить сервер:
```
python manage.py migrate
python manage.py runserver
```
## Запуск проекта в Docker контейнере
+ Установить Docker.
Параметры запуска описаны в файлах docker-compose.yml и nginx.conf которые находятся в директории infra/.

+ Запустить docker compose: 
```
docker-compose up -d --build
```
+ Cоздать миграции:
``` 
docker-compose exec backend python manage.py migrate
```
+ Загрузить ингредиенты и теги:
```
docker-compose exec backend python manage.py load_ingr_tags
```
+ Создайть суперпользователя:
``` 
docker-compose exec backend python manage.py createsuperuser
```
+ Собрать статику:
```  
docker-compose exec backend python manage.py collectstatic --noinput
```

## Запуск проекта на сервере

+ Клонировать проект с помощью git clone.
+ Перейти в папку \foodgram-project-react\backend и выполнить команды:
```
sudo docker build -t <логин на DockerHub>/<название образа для бэкенда, любое> 
sudo docker login
sudo docker push <логин на DockerHub>/<название образа для бэкенда>
``` 
+ Перейти в папку \foodgram-project-react\frontend и выполнить команды:
```
sudo docker build -t <логин на DockerHub>/<название образа для фронтэнда, любое> 
sudo docker login
sudo docker push <логин на DockerHub>/<название образа для фронтэнда> 
```
+ Установить docker на сервер:
`sudo apt install docker.io`
+ Установить docker-compose на сервер:
```
sudo apt-get update
sudo apt install docker-compose
```
+ Скопировать файл docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```
+ Добавить в Secrets GitHub переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>
USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ>
TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```
+ На сервере - создать и применить миграции, собрать статику, создать суперпользователя, загрузить список ингредиентов:
```
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic --no-input 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py loaddata ingredients.json
```
Проект будет доступен по вашему IP-адресу.

### Автор

[Громова Наталия](https://github.com/Nataliya-miyau) - бэкенд и деплой.

Фронтенд предоставлен платформой [ЯндексПрактикум](https://github.com/yandex-praktikum)

