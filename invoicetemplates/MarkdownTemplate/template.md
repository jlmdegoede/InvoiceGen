# {{ TITLE }}
### Gegevens factuur

| | |
|-|-|
|Volgnummer|{{ INVOICE_NUMBER }}|
|Datum|{{ DATE }}|
|Vervaldatum|{{ EXPIRATION_DATE }}|


### Opdrachtnemer

| | |
|-|-|
|Naam|{{ SUPPLIER_NAME }}|
|Adres|{{ SUPPLIER_ADDRESS }}|
|Plaats en postcode|{{ SUPPLIER_CITY_AND_ZIPCODE }}|
|E-mailadres|{{ SUPPLIER_EMAIL }}|
|KvK|{{ SUPPLIER_KVK }}|
|BTW-nummer|{{ SUPPLIER_BTW }}|
|IBAN|{{ SUPPLIER_IBAN }}|


### Opdrachtgever

| | |
|-|-|
|Opdrachtgever|{{ COMPANY_NAME }} |
|Adres|{{ COMPANY_ADDRESS }}|
|Plaats en postcode|{{ COMPANY_CITY_AND_ZIPCODE }}|


### Geleverd

|Opdracht|Volgnummer|Kwantiteit|Prijs per eenheid|Prijs|
|-|-|-|-|
{{ ORDER_INSERT }}

- Subtotaal: &#8364;{{ SUBTOTAL }}

- BTW: &#8364;{{ BTW }}

- Totaal te voldoen: &#8364;{{ TOTAL }}

