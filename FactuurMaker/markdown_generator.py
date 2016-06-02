__author__ = 'joche'


def create_markdown_file(naam, bedrijf, date, articles, volgnummer):
    markdown_file = "# Factuur " + str(date) + "\n"
    markdown_file += "## Freelancer " + naam.naam + "\n"
    markdown_file += "### Gegevens factuur\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Volgnummer|" + str(volgnummer) + "|\n" + "|Datum|"+ str(date) + "|\n"
    markdown_file += "\n\n### Gegevens leverancier\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Naam|" + naam.naam + "|\n" + "|Adres|"+ naam.adres + " " + naam.plaats_en_postcode + "|\n|E-mail|" + naam.emailadres + "|\n|IBAN|"+ naam.iban + "|\n"
    markdown_file += "\n\n### Gegevens afnemer\n"
    markdown_file += "\n| | |\n|-|-|\n" + "|Bedrijfsnaam|" + bedrijf.bedrijfsnaam + "|\n|Adres|" + bedrijf.bedrijfsadres + " " + bedrijf.bedrijfsplaats_en_postcode + "|\n"
    markdown_file += "\n\n### Geleverd\n"
    markdown_file += "\n|Artikel|Blad/nummer|Kwantiteit|Prijs|\n"
    markdown_file += "|-|-|-|-|\n"
    totaalbedrag = 0

    if not isinstance(articles, list):
        articles = articles.all()
    for article in articles:
        totaalbedrag += article.word_count * article.word_price
        markdown_file = markdown_file + "|"+ article.title +"|"+ article.magazine + "/" + str(article.magazine_number) + "|" + str(article.word_count) + " woorden| &#8364;" + str(article.word_count * article.word_price) + "|\n"
    markdown_file = markdown_file + "Totaal te voldoen: &#8364;" + str(totaalbedrag)

    return markdown_file
