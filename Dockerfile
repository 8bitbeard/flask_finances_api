
# FROM python:3.8.0-alpine

# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /usr/src/app/requirements.txt

# RUN \
#     apk add --no-cache postgresql-libs libstdc++ && \
#     apk add --no-cache --virtual .build-deps gcc g++ musl-dev postgresql-dev && \
#     python3 -m pip install -r requirements.txt --no-cache-dir && \
#     apk --purge del .build-deps

# COPY . /usr/src/app/

# RUN ls -la src/

# EXPOSE 5000

# RUN chmod u+x ./docker-entrypoint.sh
# ENTRYPOINT ["sh", "./docker-entrypoint.sh"]


FROM ubuntu:latest

RUN \
    apt-get update -y && \
    apt-get install -y python3-pip python3 libpq-dev locales -y && \
    locale-gen pt_BR.UTF-8 && \
    update-locale LANG=pt_BR.UTF-8

ENV LANG en_US.UTF-8

# COPY ./requirements.txt /usr/src/app/requirements.txt
COPY . /usr/src/app/

WORKDIR /usr/src/app

RUN pip install -r ./requirements.txt


EXPOSE 5000

RUN chmod u+x ./docker-entrypoint.sh
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
