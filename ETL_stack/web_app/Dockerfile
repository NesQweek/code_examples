FROM python:3.11-alpine3.16

# Копируем файл requirements.txt внутрь контейнера
COPY requirements.txt /temp/requirements.txt

# Установить все зависимости для postgres
RUN apk add postgresql-client build-base postgresql-dev

# Установить остальные зависимости для веб-сервиса 
RUN pip install -r /temp/requirements.txt

COPY django_service /service

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /service
EXPOSE 8000


RUN adduser --disabled-password service-user

USER service-user
