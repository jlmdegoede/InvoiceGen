#!/usr/bin/env bash
python3 manage.py migrate
python3 manage.py loaddata fixtures/*.json
python3 manage.py createautoadmin
bower install --allow-root
python3 manage.py collectstatic --no-input
daphne -b 0.0.0.0 -p 8000 InvoiceGen.asgi:channel_layer