FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk --update add bash nano gcc

RUN pip install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt

RUN pip install -r /var/www/requirements.txt

ENV ALERTING_SECRET_PATH=/app/secret.yaml

COPY . /app
