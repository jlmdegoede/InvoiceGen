#!/usr/bin/env bash
python3 manage.py migrate
python3 manage.py loaddata fixtures/*.json
daphne -b 0.0.0.0 -p 8000 InvoiceGen.asgi:channel_layer