FROM alpine

RUN apk add python3 py3-pip

RUN mkdir /chatserver

WORKDIR /chatserver/

EXPOSE 65432
