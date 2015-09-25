__author__ = 'joche'
#Factuur 27-07-2015
## Freelancer Jochem de Goede

### Gegevens factuur
#| | |
#|-|-|
#|Volgnummer|37|
#|Datum|27-07-2015|


### Gegevens leverancier
#| | |
#|-|-|
#|Naam|Jochem de Goede|
#|Adres|Balthasar van der Polweg 374, 2628 AZ Delft|
#|E-mail|jochem@degoede.email|
#|IBAN|NL23 INGB 0659 3626 35|

### Gegevens afnemer
#| | |
#|-|-|
#|Bedrijfsnaam|Reshift Digital|
#|Adres|Richard Holkade 8, 2033 PZ Haarlem|
#|Website|[reshift.nl](http://reshift.nl)

### Geleverd
#|Artikel|Blad/nummer|Kwantiteit|Prijs|
#|-|-|-|
#|10 tips voor Windows 10|PCM / 8| 2500 woorden| 625 euro|
#|3 x Miniworkshops | PCM / 8| 1500 woorden | 375 euro |

#**Totaal te voldoen: 1000 euro**

def create_markdown_file(naam, bedrijf, date, articles, volgnummer):
    markdown_file = "# Factuur " + str(date) + "\n"
    markdown_file = markdown_file + "## Freelancer " + naam.naam + "\n"
    markdown_file = markdown_file +"### Gegevens factuur\n"
    markdown_file = markdown_file +"| | |\n"
    markdown_file = markdown_file + "|-|-|\n|Volgnummer|" + str(volgnummer) + "|\n" + "|Datum|"+ str(date) + "|\n"
    markdown_file = markdown_file +"\n\n### Gegevens leverancier\n"
    markdown_file = markdown_file +"| | |\n"
    markdown_file = markdown_file + "|-|-|\n|Naam|" + naam.naam + "|\n" + "|Adres|"+ naam.adres + " " + naam.woonplaats + "|\n|E-mail|" + naam.emailadres + "|\n|IBAN|"+ naam.iban + "|\n"
    markdown_file = markdown_file + "\n\n### Gegevens afnemer\n"
    markdown_file = markdown_file + "\n| | |\n|-|-|\n" + "|Bedrijfsnaam|" + bedrijf.bedrijfsnaam + "|\n|Adres|" + bedrijf.bedrijfsadres + " " + bedrijf.bedrijfsplaats + "|\n"
    markdown_file = markdown_file + "\n\n### Geleverd\n"
    markdown_file = markdown_file + "\n|Artikel|Blad/nummer|Kwantiteit|Prijs|\n"
    markdown_file = markdown_file + "|-|-|-|-|\n"
    totaalbedrag = 0
    if (not isinstance(articles, list)):
        articles = articles.all()
    for article in articles:
        totaalbedrag += article.word_count * 0.25
        markdown_file = markdown_file + "|"+ article.title +"|"+ article.magazine + "/" + str(article.magazine_number) + "|" + str(article.word_count) + " woorden| &#8364;" + str(article.word_count * 0.25) + "|\n"
    markdown_file = markdown_file + "Totaal te voldoen: &#8364;" + str(totaalbedrag)
    return markdown_file