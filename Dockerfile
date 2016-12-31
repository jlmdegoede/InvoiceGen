FROM python:3.5
ENV REDIS_HOST "redis"
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor
ADD . /invoicegen
WORKDIR /invoicegen
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN pip install -r requirements.txt
