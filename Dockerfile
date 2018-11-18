FROM python:3.7.1-alpine3.8 as builder

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
