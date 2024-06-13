1) Создание .gitignore, requirements.txt
2) Создание папки для django сервиса ./web/django_service
3) Создание Dockerfile в ./web_app
4) Запуск docker compose build в ./web_app
5) Создание docker-compose.yml в ./web_app
6) Запуск docker compose run --rm web-app sh -c "django-admin startproject service ." в ./web_app
"." создаст проект в текущей директории в которой выполняется команда

commit > init_branch

7) Запуск docker compose up, можно перейти на localhost по 8000 порту и проверить django
Также по умолчанию создается db.sqlite3, удаляю её

commit > change_db_branch
merge > change_db_branch > master

8) Модификация docker-compose.yml с добавлением нового сервиса database с указанием ссылки на неё в сервис web-app (environment DB_HOST=database) и указанием depends on
9) Изменения в settings.py и затем docker compose build и затем docker compose up
10) т.к. интерпретатор не определен будет ошибка с модулем os, cmd+shift+p >select interpretator
добавить драйвер postgres в requirements psycorg, прописать файл с установкой зависимостей python к postgres RUN apk add postgresql-client build-base postgresql-dev # 3 пакета
11) docker compose build, docker compose up и сервис подключится к postgres

commit > change_db_branch

12) далее нужно применить миграции на базе postgres docker-compose run --rm  web-app sh -c "python manage.py migrate"
Задать суперпользователя docker-compose run --rm  web-app sh -c "python manage.py createsuperuser"
login: admin
email:
password: admin

13) теперь можно залогиниться http://127.0.0.1:8000/admin

14) создание сервиса
 docker-compose run --rm  web-app sh -c "python manage.py startapp prediction"

написать код для models.py, views.py и тд.

docker-compose run --rm  web-app sh -c "./manage.py makemigrations clients"
docker-compose run --rm  web-app sh -c "./manage.py migrate clients"      

15) теперь зарегестрировать модели в админке admin.py
16) После зайти в http://127.0.0.1:8000/admin и можно увидеть что django модели отображаются в админке
Также проверить другие адреса из URLs
17) запустить тестовый скрипт для отправки предсказания по API

commit > create_app_branch
