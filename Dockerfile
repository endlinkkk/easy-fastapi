FROM python:3.12 AS builder

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y nginx curl


# Копируем файлы poetry для установки зависимостей
COPY pyproject.toml poetry.lock /

RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем исходный код и другие файлы
COPY src /app/src
COPY static /usr/share/nginx/html/static
COPY nginx.conf /etc/nginx/nginx.conf
COPY tests /app/tests

# Устанавливаем рабочую директорию
WORKDIR /app

# Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]