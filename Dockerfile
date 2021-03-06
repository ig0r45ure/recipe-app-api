FROM python:3.7-alpine
MAINTAINER ig0r45ure

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

ENV PATH=$PATH:/home/user/.local/bin:/usr/local/lib/python3.7/site-packages
RUN echo $PATH

RUN pip3 install -r ./requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
