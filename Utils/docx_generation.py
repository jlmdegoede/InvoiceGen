from docx import Document
from docx.shared import Inches
from Utils.date_helper import get_formatted_string

def generate_docx_invoice(invoice, user, products, tax_rate):
    document = Document()
    p = document.add_paragraph()
    p.add_run(user.name)
    p.add_run('\n' + user.address)
    p.add_run('\n' + user.city_and_zipcode)
    p.add_run('\n' + user.iban)

    p = document.add_paragraph()
    p.add_run(invoice.to_company.company_name)
    p.add_run('\n' + invoice.to_company.company_address)
    p.add_run('\n' + invoice.to_company.company_city_and_zipcode)

    document.add_heading(invoice.title, 0)
    document.add_paragraph(
        'Volgnummer: \t' + str(invoice.invoice_number), style='ListBullet'
    )
    document.add_paragraph(
        'Factuurdatum: \t' + get_formatted_string(invoice.date_created), style='ListBullet'
    )
    document.add_paragraph(
        'Vervaldatum: \t' + get_formatted_string(invoice.expiration_date), style='ListBullet'
    )
    document.add_paragraph()

    table = document.add_table(rows=1, cols=4)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Opdracht'
    hdr_cells[1].text = 'Identificatienr.'
    hdr_cells[2].text = 'Kwantiteit'
    hdr_cells[3].text = 'Prijs'
    for product in products:
        row_cells = table.add_row().cells
        row_cells[0].text = str(product.title)
        row_cells[1].text = str(product.identification_number)
        row_cells[2].text = str(product.quantity)
        row_cells[3].text = '€' + str(product.get_price())

    document.add_paragraph()

    if tax_rate:
        p = document.add_paragraph()
        run = p.add_run()
        run.add_break()
        p.add_run('Subtotaal: \t €' + str(invoice.get_totaalbedrag()))
        p.alignment = 2
        p.add_run('\nBTW: \t\t €' + str(invoice.get_btw()))
        p.alignment = 2
        p.add_run('\nTotaal te voldoen: \t €' + str(invoice.get_totaalbedrag() + invoice.get_btw()))
        p.alignment = 2
    else:
        document.add_paragraph('Totaal te voldoen: \t €' + str(invoice.get_totaalbedrag()))

    document.add_paragraph()
    document.add_paragraph('Gelieve uw betaling uiterlijk te voldoen op ' + get_formatted_string(invoice.expiration_date) + ' op IBAN ' + user.iban)

    document.add_page_break()
    return document