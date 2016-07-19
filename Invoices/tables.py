import django_tables2 as tables
from .models import Invoice, IncomingInvoice, OutgoingInvoice


class InvoiceTable(tables.Table):
    invoice_number = tables.Column(verbose_name='Volgnr.')
    title = tables.Column(verbose_name='Titel')
    date_created = tables.Column(verbose_name='Aangemaakt op')
    paid = tables.BooleanColumn(verbose_name='Betaald')

    class Meta:
        pass


class IncomingInvoiceTable(InvoiceTable):
    subtotal = tables.Column(verbose_name='Subtotaal')
    btw = tables.Column(verbose_name='BTW')
    actions = tables.TemplateColumn('<a href="{% url "edit_incoming_invoice" record.id %}"><i class="material-icons">edit</i></a><a href="#" class="modal-trigger delete" value="{{ record.id }}"><i class="material-icons">delete</i></a>', verbose_name='')

    class Meta:
        model = IncomingInvoice
        fields = ('invoice_number', 'title', 'date_created', 'paid', 'subtotal', 'btw', 'actions', )
        attrs = {'class': 'striped responsive-table'}


class OutgoingInvoiceTable(InvoiceTable):
    total_amount = tables.Column(verbose_name='Bedrag')
    actions = tables.TemplateColumn('<a href="{% url "edit_outgoing_invoice" record.id %}"><i class="material-icons">edit</i></a><a href="#modal1" class="modal-trigger delete" value="{{ record.id }}"><i class="material-icons">delete</i></a>', verbose_name='')

    class Meta:
        model = IncomingInvoice
        attrs = {'class': 'striped responsive-table'}
        fields = ('invoice_number', 'title', 'date_created', 'paid', 'total_amount', 'actions',)