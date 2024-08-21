#pull offocial base image
FROM python:3.9.7-alpine

#set work directory
WORKDIR /user/src/app

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add postgresql-dev python3-dev musl-dev zlib-dev jpeg-dev

COPY . /user/src/app

#install dependecies
RUN pip install --update pip
RUN pip install -r requirements.txt