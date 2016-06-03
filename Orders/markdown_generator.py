
def create_markdown_file(naam, bedrijf, date, articles, volgnummer, with_tax_rate):
    markdown_file = "# Factuur " + str(date) + "\n"
    markdown_file += "## Freelancer " + naam.naam + "\n"
    markdown_file += "### Gegevens factuur\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Volgnummer|" + str(volgnummer) + "|\n" + "|Datum|"+ str(date) + "|\n"
    markdown_file += "\n\n### Opdrachtnemer\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Naam|" + naam.naam + "|\n" + "|Adres|"+ naam.adres + "|\n|Plaats en postcode|" + naam.plaats_en_postcode + "|\n|E-mailadres|" + naam.emailadres + "|\n|IBAN|"+ naam.iban + "|\n"
    markdown_file += "\n\n### Opdrachtgever\n"
    markdown_file += "\n| | |\n|-|-|\n" + "|Opdrachtgever|" + bedrijf.company_name + "|\n|Adres|" + bedrijf.company_address + " |\n|Plaats en postcode|" + bedrijf.company_city_and_zipcode + "|\n"
    markdown_file += "\n\n### Geleverd\n"
    markdown_file += "\n|Opdracht|Volgnummer|Kwantiteit|Prijs|\n"
    markdown_file += "|-|-|-|-|\n"
    totaalbedrag = 0
    btw_hoeveelheid = 0
    totaal_met_btw = 0

    if not isinstance(articles, list):
        articles = articles.all()
    if with_tax_rate:
        for article in articles:
            totaalbedrag += article.quantity * article.price_per_quantity
            btw_hoeveelheid += (article.quantity * article.price_per_quantity) * (float(article.tax_rate / 100))
            markdown_file = markdown_file + "|"+ article.title +"|"+ str(article.identification_number) + "|" + str(article.quantity) +  "| &#8364;" + str(article.quantity * article.price_per_quantity) + "|\n"
        totaal_met_btw = totaalbedrag + btw_hoeveelheid
        markdown_file = markdown_file + '\n'
        markdown_file = markdown_file + "- Subtotaal: &#8364;" + str(totaalbedrag) + "\n\n"
        markdown_file = markdown_file + "- BTW: &#8364;" + str(btw_hoeveelheid) + "\n\n"
        markdown_file = markdown_file + "- Totaal te voldoen: &#8364;" + str(totaal_met_btw) + "\n\n"
    else:
        for article in articles:
            totaalbedrag += article.quantity * article.price_per_quantity
            markdown_file = markdown_file + "|"+ article.title +"|"+ str(article.identification_number) + "|" + str(article.quantity) +  "| &#8364;" + str(article.quantity * article.price_per_quantity) + "|\n"
        markdown_file = markdown_file + "- Totaal te voldoen: &#8364;" + str(totaalbedrag)

    return markdown_file
