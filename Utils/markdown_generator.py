def create_markdown_file(invoice, user, company, date, products, with_tax_rate):
    markdown_file = "# " + invoice.title + "\n"
    markdown_file += "### Gegevens factuur\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Volgnummer|" + str(invoice.invoice_number) + "|\n" + "|Datum|" + str(date) + "|\n"
    markdown_file += "\n\n### Opdrachtnemer\n"
    markdown_file += "| | |\n"
    markdown_file += "|-|-|\n|Naam|" + user.name
    markdown_file += "|\n" + "|Adres|" + user.address
    markdown_file += "|\n|Plaats en postcode|" + user.city_and_zipcode
    markdown_file += "|\n|E-mailadres|" + user.email
    if user.kvk:
        markdown_file += "|\n|KvK|" + user.kvk
    if user.btw_number:
        markdown_file += "|\n|BTW-nummer|" + user.btw_number
    markdown_file += "|\n|IBAN|" + user.iban + "|\n"
    markdown_file += "\n\n### Opdrachtgever\n"
    markdown_file += "\n| | |\n|-|-|\n" + "|Opdrachtgever|" + company.company_name + "|\n|Adres|" + company.company_address + " |\n|Plaats en postcode|" + company.company_city_and_zipcode + "|\n"
    markdown_file += "\n\n### Geleverd\n"
    markdown_file += "\n|Opdracht|Volgnummer|Kwantiteit|Prijs|\n"
    markdown_file += "|-|-|-|-|\n"

    if not isinstance(products, list):
        products = products.all()
    if with_tax_rate:
        for product in products:
            markdown_file += "|" + product.title + "|" + str(product.identification_number) + "|" + str(
                product.quantity) + "| &#8364;" + str(product.get_price()) + "|\n"
        markdown_file += '\n'
        markdown_file += "- Subtotaal: &#8364;" + str(invoice.get_totaalbedrag()) + "\n\n"
        markdown_file += "- BTW: &#8364;" + str(invoice.get_btw()) + "\n\n"
        markdown_file += "- Totaal te voldoen: &#8364;" + str(invoice.get_totaalbedrag() + invoice.get_btw()) + "\n\n"
    else:
        for product in products:
            markdown_file = markdown_file + "|" + product.title + "|" + str(product.identification_number) + "|" + str(
                product.quantity) + "| &#8364;" + str(product.get_price()) + "|\n"
        markdown_file = markdown_file + "- Totaal te voldoen: &#8364;" + str(invoice.get_totaalbedrag())

    return markdown_file
