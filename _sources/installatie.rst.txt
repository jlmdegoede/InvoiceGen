
Installatie
===========

Je kunt Invoicegen op twee manieren installeren: direct op de server (Linux of macOS) of door middel van Docker. Die laatste manier wordt aanbevolen, gezien die het eenvoudigste is.


Docker
------
We gaan er vanuit dat je Docker al hebt geïnstalleerd op je favoriete platform.
Daarna is het als eerste nodig om een postgres-container binnen te halen en te starten:

- `docker pull postgres && docker pull jlmdegoede/invoicegen`
- `docker run --name igpostgres -d postgres`.

Vervolgens start je Invoicegen met
- `docker run -d -e SECRET_KEY=<je-geheime-sleutel> --link igpostgres:postgres -p 80:80 jlmdegoede/invoicegen`

Zorg dat je een goede geheime sleutel invult. Je kunt er bijvoorbeeld hier_ een genereren.
Ga in de browser naar http://127.0.0.1 om in te loggen.

Voor in productie map je de container naar een andere poort met `-p 8000:80` en zet je er apache of nginx voor met https.

.. _hier: http://www.miniwebtool.com/django-secret-key-generator/


Directe installatie
-------------------

Je kunt Invoicegen ook direct installeren zonder Docker, maar dan is het wel nodig om veel software te installeren.
Zorg ervoor dat je postgresql, redis-server, nodejs-legacy en python3 met pip hebt geïnstalleerd. Kloon de git-repository met:

- `git clone https://github.com/jlmdegoede/Invoicegen.git`
- `cd Invoicegen`

Maak een bestand `.env` en plaats daarin `SECRET_KEY=<je-secret-key>` die je bijvoorbeeld vanaf hier_ genereert.

Installeer de Python-dependencies met:

- optioneel: maak eerst een virtualenv met: `virtualenv -p python3 ~/.venvig`
- optioneel: activeer de virtualenv met `source ~/.venvig/bin/activate`
- `pip3 install -r requirements.txt`

Verzamel de statische dependencies:

- `npm install -g bower`
- `bower install`
- `python3 manage.py collectstatic`

Kickstart de database en genereer de eerste admin:

- `python3 manage.py migrate`
- `python3 manage.py createautoadmin`

Daarna kun je supervisord gebruiken uit de map config/ om Daphne, Celery en een aantal workers te starten. Met nginx of apache zet je dan een reverse-proxy op naar poort 8000. Zorg ervoor dat je ook websockets doorstuurt naar Invoicegen.

