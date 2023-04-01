FROM python:3.9-alpine3.13
# The MAINTAINER command is deprecated
LABEL maintainer="hotamul9@gmail.com"

# Python that you don't want to buffer the output
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./application /application
WORKDIR /application

ARG DEV=false
RUN python -m venv /venv && \
    apk add --update --no-cache jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base linux-headers musl-dev zlib zlib-dev sqlite-dev && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install wheel && \
    /venv/bin/pip install --use-pep517 -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then \
        /venv/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /var/www/share-blog/static/media && \
    chown -R django-user:django-user /var /application/log && \
    chmod -R 755 /var /application/log

COPY ./override/base.py /venv/lib64/python3.7/site-packages/django/db/backends/sqlite3/base.py

ENV PATH="/venv/bin:$PATH"

USER django-user