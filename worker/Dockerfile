FROM python:3.8

EXPOSE 8080 8946

RUN apt-get update

RUN apt-get install -y --no-install-recommends software-properties-common

RUN echo "deb [trusted=yes] https://repo.fury.io/distribworks/ /" > \
/etc/apt/sources.list.d/fury.list

RUN apt-get update

RUN apt-get install -y --no-install-recommends dnsutils bash dkron ca-certificates openssl tzdata jq

RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./ /app

ENV ALERTING_SECRET_PATH=/app/secret.yaml

ENTRYPOINT ["dkron"]

CMD ["--help"]
