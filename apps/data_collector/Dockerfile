FROM ubuntu:latest
MAINTAINER Jiangwen Su "uukuguy@gmail.com"

RUN apt-get update && apt-get install -y python-pip python-dev
RUN pip install --upgrade pip
RUN pip install --upgrade msgpack-python pymongo thrift

ADD src /apps/data_collector/src
ADD utils /apps/data_collector/utils

VOLUME ["/data"]

EXPOSE 20161

WORKDIR '/apps/data_collector'
ENTRYPOINT './src/server.py'

