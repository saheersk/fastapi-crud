FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /blog-app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

