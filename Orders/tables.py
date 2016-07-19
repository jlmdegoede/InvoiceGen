import django_tables2 as tables
from .models import Product


class OrderTable(tables.Table):
    check = tables.TemplateColumn(
        '<input type="checkbox" id="{{ record.id }}" value="{{ record.id }}" name="to_invoice" /><label for="{{ record.id }}"></label>',
        verbose_name='')
    title = tables.TemplateColumn(
        "<a href='{% url 'view_product' record.id record.title|slugify %}'>{{ record.title }}</a>",
        verbose_name="Opdrachten")
    date_deadline = tables.Column(verbose_name="Deadline")
    quantity = tables.Column(verbose_name="Aantal")
    from_company = tables.Column(verbose_name="Opdrachtgever")
    invoice = tables.Column(verbose_name="Gefactureerd")
    actions = tables.TemplateColumn(
        '<a href="{% url "edit_product" record.id %}"><i class="material-icons">edit</i></a><a href="#modal1" class="modal-trigger delete" value="{{ record.id }}" name="{{ record.title }}"><i class="material-icons">delete</i></a>',
        verbose_name='')

    class Meta:
        model = Product
        attrs = {'class': 'striped responsive-table'}
        fields = ('check', 'title', 'quantity', 'date_deadline', 'from_company', 'invoice')
