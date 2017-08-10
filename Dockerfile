FROM ubuntu:16.04
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y install nginx texlive supervisor nodejs-legacy npm python3 python3-pip git python3-setuptools

ADD requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir /invoicegen
ADD . /invoicegen
WORKDIR /invoicegen

RUN adduser --disabled-password --gecos '' workeruser
RUN npm install bower -g

RUN cp supervisord.conf /etc/supervisor.conf

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/*
RUN cp config/nginx/invoicegen.conf /etc/nginx/sites-available/invoicegen.conf
RUN ln -s /etc/nginx/sites-available/invoicegen.conf /etc/nginx/sites-enabled/invoicegen.conf
EXPOSE 80

CMD ["./docker-entrypoint.sh"]