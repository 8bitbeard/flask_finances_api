# syntax=docker/dockerfile:1

# FROM python:3.9-alpine3.14

# WORKDIR /app

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

# COPY . .

FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN \
    apk add --no-cache postgresql-libs libstdc++ && \
    apk add --no-cache --virtual .build-deps gcc g++ musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]