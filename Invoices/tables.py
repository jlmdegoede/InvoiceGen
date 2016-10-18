import django_tables2 as tables
from .models import Invoice, IncomingInvoice, OutgoingInvoice
from django_tables2 import A

class InvoiceTable(tables.Table):
    date_created = tables.Column(verbose_name='Aangemaakt op')
    paid = tables.BooleanColumn(verbose_name='Betaald')

    class Meta:
        pass


class IncomingInvoiceTable(InvoiceTable):
    invoice_number = tables.LinkColumn('detail_incoming_invoice', args=[A('pk')], verbose_name='Volgnr.')
    title = tables.LinkColumn('detail_incoming_invoice', args=[A('pk')], verbose_name='Titel')
    subtotal = tables.TemplateColumn("€ {{ value }}", verbose_name='Subtotaal')
    btw_amount = tables.TemplateColumn("€ {{ value }}", verbose_name='BTW')
    actions = tables.TemplateColumn('<a href="{% url "edit_incoming_invoice" record.id %}"><i class="material-icons">edit</i></a><a href="#" class="modal-trigger delete" value="{{ record.id }}"><i class="material-icons">delete</i></a>', verbose_name='')

    class Meta:
        model = IncomingInvoice
        fields = ('invoice_number', 'title', 'date_created', 'paid', 'subtotal', 'btw_amount', 'actions', )
        attrs = {'class': 'striped responsive-table'}


class OutgoingInvoiceTable(InvoiceTable):
    invoice_number = tables.LinkColumn('detail_outgoing_invoice', args=[A('pk')], verbose_name='Volgnr.')
    title = tables.LinkColumn('detail_outgoing_invoice', args=[A('pk')], verbose_name='Titel')
    get_total_amount = tables.TemplateColumn("€ {{ value|floatformat:2 }}", verbose_name='Bedrag')
    actions = tables.TemplateColumn('<a href="{% url "edit_outgoing_invoice" record.id %}"><i class="material-icons">edit</i></a><a href="#modal1" class="modal-trigger delete" value="{{ record.id }}"><i class="material-icons">delete</i></a>', verbose_name='')

    class Meta:
        model = IncomingInvoice
        attrs = {'class': 'striped responsive-table'}
        fields = ('invoice_number', 'title', 'date_created', 'paid', 'get_total_amount', 'actions',)
