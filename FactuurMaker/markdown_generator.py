
def create_markdown_file(naam, bedrijf, date, articles, volgnummer):
    markdown_file = "# Factuur " + str(date) + "\n"
    markdown_file += "## Freelancer " + naam.naam + "\n"
    markdown_file += "### Gegevens factuur\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Volgnummer|" + str(volgnummer) + "|\n" + "|Datum|"+ str(date) + "|\n"
    markdown_file += "\n\n### Gegevens leverancier\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Naam|" + naam.naam + "|\n" + "|Adres|"+ naam.adres + "|\n|Plaats en postcode|" + naam.plaats_en_postcode + "|\n|E-mailadres|" + naam.emailadres + "|\n|IBAN|"+ naam.iban + "|\n"
    markdown_file += "\n\n### Gegevens opdrachtgever\n"
    markdown_file += "\n| | |\n|-|-|\n" + "|Opdrachtgever|" + bedrijf.bedrijfsnaam + "|\n|Adres|" + bedrijf.bedrijfsadres + " |\n|Plaats en postcode|" + bedrijf.bedrijfsplaats_en_postcode + "|\n"
    markdown_file += "\n\n### Geleverd\n"
    markdown_file += "\n|Opdracht|Volgnummer|Kwantiteit|Prijs|\n"
    markdown_file += "|-|-|-|-|\n"
    totaalbedrag = 0

    if not isinstance(articles, list):
        articles = articles.all()
    for article in articles:
        totaalbedrag += article.quantity * article.price_per_quantity
        markdown_file = markdown_file + "|"+ article.title +"|"+ str(article.identification_number) + "|" + str(article.quantity) +  "| &#8364;" + str(article.quantity * article.price_per_quantity) + "|\n\n"
    markdown_file = markdown_file + "Totaal te voldoen: &#8364;" + str(totaalbedrag)

    return markdown_file
