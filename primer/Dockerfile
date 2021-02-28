FROM alpine

RUN apk --update --no-cache add bash nano gcc python3 py3-pip

RUN pip3 install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt

RUN pip install -r /var/www/requirements.txt --ignore-installed six

ENV ALERTING_SECRET_PATH=/app/secret.yaml

COPY . /app

CMD ["/app/run.sh"]
