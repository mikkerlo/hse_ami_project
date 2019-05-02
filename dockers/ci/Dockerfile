FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
        libffi-dev jpeg-dev zlib-dev git

RUN apk add --update py-pip

RUN pip3 install flake8 \
    pep8-naming \
    flake8-comprehensions \
    flake8-pep3101 \
    flake8-pyi \
    flake8-quotes \
    flake8-mutable

