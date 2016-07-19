import django_tables2 as tables
from .models import Company


class CompanyTable(tables.Table):
    company_name = tables.Column(verbose_name='Naam')
    company_address = tables.Column(verbose_name='Adres')
    company_city_and_zipcode = tables.Column(verbose_name='Plaats en postcode')
    recent_products = tables.TemplateColumn('{% for product in record.recent_products %} <a href="#" value="{{ product.id }}" class="modal-trigger dialog-trigger">{{ product.title }}</a> {% endfor %}', verbose_name='Recente opdrachten')
    actions = tables.TemplateColumn('<a href="{% url "company_edit" record.id %}"><i class="material-icons">edit</i></a><a href="#" class="modal-trigger delete" value="{{ record.id }}" name="{{ record.company_name }}"><i class="material-icons">delete</i></a>', verbose_name='')

    class Meta:
        model = Company
        attrs = {'class': 'striped responsive-table'}
        fields = ('company_name', 'company_address', 'company_city_and_zipcode', 'recent_products')