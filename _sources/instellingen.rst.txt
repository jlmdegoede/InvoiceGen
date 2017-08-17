Instellingen & Statistieken
===========================

Onder het menu *Meer* vind je nog een aantal opties, waaronder *Statistieken* en *Instellingen*.

Instellingen
------------
De instellingen zijn zijdelings bij de andere onderdelen al een beetje langsgekomen, maar het kan geen kwaad ze nog even door te nemen

Persoonlijke gegevens
~~~~~~~~~~~~~~~~~~~~~~
Bij de persoonlijke gegevens kun je je naw-gegevens instellen, evenals IBAN en eventueel KvK- en btw-nummer. Deze gegevens worden automatisch op je facturen gezet. Zonder deze gegevens kunnen geen facturen gegenereerd worden.

Algemene instellingen
~~~~~~~~~~~~~~~~~~~~~
Op de algemene instellingen kun je de website-url instellen (zorg dat deze goedstaat voor het genereren van linkjes), de websitenaam die rechtsboven en in de titelbalk moet worden weergegeven en je bedrijfskleuren voor boven en onder kiezen. Ook kun je hier je api-keys voor bunq en mollie instellen.

Factuursjablonen
~~~~~~~~~~~~~~~~
Op de pagina Factuursjablonen kun je je sjablonen kiezen. Op dit moment is er echter voor pdf en docx nog maar een sjabloon.

Toch is het maken van een sjabloon erg eenvoudig, voor in ieder geval docx. Download de voorbeeld docx_ en pas deze naar je wens aan. Zorg er wel voor dat de variabelen zoals in het document aanwezig blijven. Heb je alle wijzigingen gemaakt, dan plaats je je nieuwe template in de map `Invoicetemplates/<je-sjabloon-naam>`. Ga dan naar `/admin` en dan naar *Invoice templates* en klik op *Invoice template toevoegen*. Vul een naam in voor je template, de locatie is *<je-sjabloon-naam>* van net en de main file is de naam van je docx-bestand. Order-template kun je leeglaten voor docx-templates. Kies bij *Template type* voor *DOCX* en upload een previewafbeelding van je template. Klik op *Opslaan* en je nieuwe template verschijnt bij de factuursjablonen. Klik op *Als standaard instellen* om deze altijd te gebruiken.

Gebruikers
~~~~~~~~~~
Bij gebruikers kun je nieuwe gebruikers toevoegen en de rechten beheren van bestaande gebruikers.

Statistieken
------------
Op de pagina statistieken zie je een aantal cijfers van het aantal opdrachten, aantal inkomsten en meer.


E-mail
------
Op de pagina mail zie je alle verzonden e-mailberichten binnen in het systeem. Je kunt hier ook nieuwe e-mailtemplates toevoegen, die je kunt gebruiken als je bijvoorbeeld een factuur wilt mailen zodat altijd hetzelfde mailtje de deur uitgaat.

.. _docx: https://github.com/jlmdegoede/Invoicegen/blob/master/invoicetemplates/WordTemplate/template.docx