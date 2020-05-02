FROM node:7
LABEL MAINTAINER Robson Miranda <mirandarfsm@gmail.com>

# NODE #
RUN npm install -g bower
RUN npm install -g grunt-cli

RUN mkdir -p /app/client

COPY ./client/bower.json /app/client/bower.json
COPY ./client/package.json /app/client/package.json

WORKDIR /app/client

RUN npm install
RUN bower install --allow-root

FROM python:3.6

RUN mkdir -p /app/server

COPY ./server/requirements.txt /app/server/requirements.txt

WORKDIR /app/server

RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install ptvsd