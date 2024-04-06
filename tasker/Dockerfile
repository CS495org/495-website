# FROM python:3.12-alpine
FROM localhost:5000/tasker

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .