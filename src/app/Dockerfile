# syntax=docker/dockerfile:1
FROM python:3.10-alpine

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "main:asgi_app", "--host", "0.0.0.0", "--port", "80"]
