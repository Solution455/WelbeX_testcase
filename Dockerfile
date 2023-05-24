# Установка базового образа Python
FROM python:3.9


# Установка рабочей директории

WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install -r requirements.txt

# Копирование проекта
COPY . .

# Команда для запуска сервера Django
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

