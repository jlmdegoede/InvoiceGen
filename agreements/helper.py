from settings.models import UserSetting
from companies.models import Company
from .constants import *


def replace_text(agree_text, products):
    user = UserSetting.objects.first()
    company = Company.objects.first()
    client_name = company.company_name
    client_city_zipcode = company.company_city_and_zipcode
    client_company_name = company.company_name
    client_address = company.company_address
    contractor_name = user.name
    contractor_city_zipcode = user.city_and_zipcode
    contractor_address = user.address

    article_text = "\n"
    for product in products:
        article_text += "Opdracht " + product.title + " met een kwantiteit van " + str(
            product.quantity) + " en een prijs van " + str(
            product.price_per_quantity) + " euro per eenheid voor opdrachtgever " + product.from_company.company_name + "\n"

    agree_text = agree_text.replace(OPDRACHT_OMSCHRIJVING_CONSTANT, article_text)
    agree_text = agree_text.replace(CLIENT_NAME_CONSTANT, client_name)
    agree_text = agree_text.replace(CLIENT_CITY_ZIPCODE_CONSTANT, client_city_zipcode)
    agree_text = agree_text.replace(CLIENT_COMPANY_NAME_CONSTANT, client_company_name)
    agree_text = agree_text.replace(CLIENT_ADDRESS_CONSTANT, client_address)
    agree_text = agree_text.replace(CONTRACTOR_ADDRESS_CONSTANT, contractor_address)
    agree_text = agree_text.replace(CONTRACTOR_CITY_ZIPCODE_CONSTANT, contractor_city_zipcode)
    agree_text = agree_text.replace(CONTRACTOR_NAME_CONSTANT, contractor_name)
    return agree_text
