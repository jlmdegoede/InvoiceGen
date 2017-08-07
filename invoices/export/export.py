import os
import subprocess
import shutil

from django.utils.crypto import get_random_string

from docxtpl import DocxTemplate

from InvoiceGen.settings import BASE_DIR
from settings.models import UserSetting
from utils.file_helper import get_temp_folder_path


class ExportInvoice(object):
    TITLE = 'TITLE'
    INVOICE_NUMBER = 'INVOICE_NUMBER'
    DATE = 'DATE'
    EXPIRATION_DATE = 'EXPIRATION_DATE'

    SUPPLIER_NAME = 'SUPPLIER_NAME'
    SUPPLIER_ADDRESS = 'SUPPLIER_ADDRESS'
    SUPPLIER_CITY_AND_ZIPCODE = 'SUPPLIER_CITY_AND_ZIPCODE'
    SUPPLIER_EMAIL = 'SUPPLIER_EMAIL'
    SUPPLIER_IBAN = 'SUPPLIER_IBAN'
    SUPPLIER_KVK = 'SUPPLIER_KVK'
    SUPPLIER_BTW = 'SUPPLIER_BTW'

    COMPANY_NAME = 'COMPANY_NAME'
    COMPANY_ADDRESS = 'COMPANY_ADDRESS'
    COMPANY_CITY_AND_ZIPCODE = 'COMPANY_CITY_AND_ZIPCODE'

    ORDER_TEMPLATE = 'ORDER_INSERT'

    ORDER_NAME = 'ORDER_NAME'
    ORDER_FOLLOW_NUMBER = 'ORDER_FOLLOW_NUMBER'
    ORDER_QUANTITY = 'ORDER_QUANTITY'
    ORDER_PRICE_PER_QUANTITY = 'ORDER_PRICE_PER_QUANTITY'
    ORDER_TOTAL_PRICE = 'ORDER_TOTAL_PRICE'

    SUBTOTAL = 'SUBTOTAL'
    BTW = 'BTW'
    TOTAL = 'TOTAL'

    def __init__(self, invoice, products, template):
        self.invoice = invoice
        self.products = products
        self.user = UserSetting.objects.first()
        self.template = template
        self.template_location = self._copy_template_to_temp()

    def generate(self):
        input = self._read_template_file()
        invoice_dictionary = self._create_dictionary()
        for key, value in invoice_dictionary.items():
            input = input.replace('{{ ' + key + ' }}', str(value))
        self._write_output_file(input)

    def _create_dictionary(self):
        order_template = self._create_product_list()

        return {self.TITLE: self.invoice.title,
                self.INVOICE_NUMBER: self.invoice.invoice_number,
                self.DATE: self.invoice.date_created,
                self.EXPIRATION_DATE: self.invoice.expiration_date,
                self.SUPPLIER_NAME: self.user.name,
                self.SUPPLIER_ADDRESS: self.user.address,
                self.SUPPLIER_CITY_AND_ZIPCODE: self.user.city_and_zipcode,
                self.SUPPLIER_EMAIL: self.user.email,
                self.SUPPLIER_IBAN: self.user.iban,
                self.SUPPLIER_KVK: self.user.kvk,
                self.SUPPLIER_BTW: self.user.btw_number,
                self.COMPANY_NAME: self.invoice.to_company.company_name,
                self.COMPANY_ADDRESS: self.invoice.to_company.company_address,
                self.COMPANY_CITY_AND_ZIPCODE: self.invoice.to_company.company_city_and_zipcode,
                self.ORDER_TEMPLATE: order_template,
                self.SUBTOTAL: self.invoice.get_total_amount(),
                self.BTW: self.invoice.get_btw(),
                self.TOTAL: self.invoice.get_total_amount_including_btw()}

    def _create_product_list(self):
        order_template = []
        for product in self.products:
            product_dict = {self.ORDER_NAME: product.title,
                            self.ORDER_FOLLOW_NUMBER: product.identification_number,
                            self.ORDER_QUANTITY: product.quantity,
                            self.ORDER_PRICE_PER_QUANTITY: product.price_per_quantity,
                            self.ORDER_TOTAL_PRICE: product.get_price()}
            product_string = self.template.order_template
            for key, value in product_dict.items():
                product_string = product_string.replace('{{ ' + key + ' }}', str(value))
            order_template.append(product_string)
        return '\n'.join(order_template)

    def _read_template_file(self):
        template_file_path = os.path.join(self.template_location, self.template.main_file)
        with open(template_file_path, 'r') as template_file:
            template_input = template_file.read()
        return template_input

    def _write_output_file(self, contents_to_write):
        template_file_path = os.path.join(self.template_location, self.template.main_file)
        with open(template_file_path, 'w') as template_file:
            template_file.write(contents_to_write)

    def _copy_template_to_temp(self):
        template_file_path = os.path.join(BASE_DIR, 'invoicetemplates', self.template.location)
        temp_location = os.path.join(get_temp_folder_path(), get_random_string(5))
        shutil.copytree(template_file_path, temp_location)
        return temp_location

    def __del__(self):
        shutil.rmtree(self.template_location)


class MarkdownExport(ExportInvoice):
    def output_filepath(self):
        return os.path.join(self.template_location, self.template.main_file)


class LatexExport(ExportInvoice):
    def generate(self):
        super(LatexExport, self).generate()
        self._compile()

    def _compile(self):
        subprocess.call([r'./compile.sh'], cwd=self.template_location)
        compiled_file = os.path.join(self.template_location, "main.pdf")
        new_pdf_location = self.output_filepath()
        shutil.move(compiled_file, new_pdf_location)

    def output_filepath(self):
        new_pdf_name = '{0}.pdf'.format(self.invoice.title)
        return os.path.join(BASE_DIR, 'temp', new_pdf_name)


class WordExport(ExportInvoice):
    def generate(self):
        invoice_dictionary = self._create_dictionary()
        doc = DocxTemplate(self.template_location + '/' + self.template.main_file)
        doc.render(invoice_dictionary)
        new_file_path = os.path.join(BASE_DIR, 'temp', self.invoice.title + '.docx')
        doc.save(new_file_path)

    def _create_product_list(self):
        order_template = []
        for product in self.products:
            product_dict = {self.ORDER_NAME: product.title,
                            self.ORDER_FOLLOW_NUMBER: product.identification_number,
                            self.ORDER_QUANTITY: product.quantity,
                            self.ORDER_PRICE_PER_QUANTITY: product.price_per_quantity,
                            self.ORDER_TOTAL_PRICE: product.get_price()}
            order_template.append(product_dict)
        return order_template

    def output_filepath(self):
        return os.path.join(BASE_DIR, 'temp', self.invoice.title + '.docx')


