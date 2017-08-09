FROM ubuntu:16.04
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y install python3 python3-pip git python3-setuptools
ADD requirements.txt .
RUN mkdir /invoicegen
ADD . /invoicegen
WORKDIR /invoicegen
RUN pip3 install -r requirements.txt
RUN adduser --disabled-password --gecos '' workeruser