FROM python:3.11 AS builder

RUN apt-get update && apt-get install -y nginx

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

COPY src /app/src

COPY static /usr/share/nginx/html/static

COPY nginx.conf /etc/nginx/nginx.conf

COPY tests /app/tests

WORKDIR app

#CMD gunicorn -k uvicorn.workers.UvicornWorker src.main:app --bind=0.0.0.0:8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]