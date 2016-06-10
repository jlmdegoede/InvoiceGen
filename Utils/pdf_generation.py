from fpdf import FPDF
from Orders.models import Product

class PDF(FPDF):
    title = None
    def header(self):
        # Arial bold 15
        self.set_font('Times', 'B', 24)
        # Title
        self.cell(0, 10, self.title, 0, 0, 'L')
        self.ln(20)

    def print_body(self, user, company, invoice):
        self.set_font('Times', 'B', 20)
        self.cell(0, 10, 'Gegevens factuur', 0, 1, 'L')
        self.set_font('Times', '', 14)

        self.cell(10)
        self.cell(40, 10, 'Datum:', 0, 0, 'L')
        self.cell(80, 10, str(invoice.date_created), 0, 1, 'L')

        self.cell(10)
        self.cell(40, 10, 'Volgnummer:', 0, 0, 'L')
        self.cell(80, 10, str(invoice.invoice_number), 0, 1, 'L')
        self.ln(10)

        self.set_font('Times', 'B', 20)
        self.cell(0, 10, 'Gegevens opdrachtnemer', 0, 1, 'L')
        self.set_font('Times', '', 14)

        self.cell(10)
        self.cell(40, 10, 'Naam:', 0, 0, 'L')
        self.cell(80, 10, user.name, 0, 1, 'L')

        self.cell(10)
        self.cell(40, 10, 'Adres:', 0, 0, 'L')
        self.cell(80, 10, user.address + ' ' + user.city_and_zipcode, 0, 1, 'L')

        self.cell(10)
        self.cell(40, 10, 'E-mail:', 0, 0, 'L')
        self.cell(80, 10, user.email, 0, 1, 'L')

        self.cell(10)
        self.cell(40, 10, 'IBAN:', 0, 0, 'L')
        self.cell(80, 10, user.iban, 0, 1, 'L')

        self.ln(10)

        self.set_font('Times', 'B', 20)
        self.cell(0, 10, 'Gegevens opdrachtgever', 0, 1, 'L')
        self.set_font('Times', '', 14)

        self.cell(10)
        self.cell(40, 10, 'Bedrijfsnaam:', 0, 0, 'L')
        self.cell(80, 10, company.company_name, 0, 1, 'L')

        self.cell(10)
        self.cell(40, 10, 'Adres:', 0, 0, 'L')
        self.cell(80, 10, company.company_address+ ' ' + company.company_city_and_zipcode, 0, 1, 'L')

        self.ln(10)

    def print_products(self, products, tax_rate):
        self.set_font('Times', 'B', 20)
        self.cell(0, 10, 'Geleverd', 0, 1, 'L')

        self.cell(10)
        self.set_font('Times', 'B', 14)
        self.cell(40, 10, 'Opdracht', 0, 0, 'L')
        self.cell(40, 10, 'Volgnummer', 0, 0, 'L')
        self.cell(40, 10, 'Kwantiteit', 0, 0, 'L')
        self.cell(40, 10, 'Prijs', 0, 0, 'L')

        self.set_font('Times', '', 14)
        totaal_bedrag = 0
        totaal_met_btw = 0
        btw = 0
        for product in products:
            totaal_bedrag += product.price_per_quantity * product.quantity
            btw = (product.quantity * product.price_per_quantity) * (float(product.tax_rate / 100))
            self.ln(10)
            self.cell(10)
            self.cell(40, 10, product.title, 0, 0, 'L')
            self.cell(40, 10, str(product.identification_number), 0, 0, 'L')
            self.cell(40, 10, str(product.quantity), 0, 0, 'L')
            self.cell(40, 10, str(product.price_per_quantity * product.quantity) + ' euro', 0, 0, 'L')

        if not tax_rate:
            self.ln(10)
            self.cell(40, 10, 'Totaal te voldoen: ' + str(totaal_bedrag) + ' euro', 0, 0, 'L')
        else:
            totaal_met_btw = totaal_bedrag + btw
            self.ln(10)
            self.cell(40, 10, 'Subtotaal:', 0, 0, 'L')
            self.cell(40, 10, str(totaal_bedrag) + ' euro', 0, 0, 'L')
            self.ln(10)
            self.cell(40, 10, 'BTW:', 0, 0, 'L')
            self.cell(40, 10, str(btw) + ' euro', 0, 0, 'L')
            self.ln(10)
            self.cell(40, 10, 'Totaal te voldoen:', 0, 0, 'L')
            self.cell(40, 10, str(totaal_met_btw) + ' euro', 0, 0, 'L')



    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def generate_pdf(products, user, invoice):
    # Instantiation of inherited class
    pdf = PDF()
    pdf.title = invoice.title
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.print_body(user, invoice.to_company, invoice)
    pdf.print_products(products, products[0].tax_rate)
    return pdf.output(dest='S').encode('latin-1')