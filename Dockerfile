FROM ubuntu:16.04
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y install texlive python3 python3-pip git python3-setuptools
ADD requirements.txt .
RUN pip3 install -r requirements.txt
RUN mkdir /invoicegen
WORKDIR /invoicegen