import django_tables2 as tables
from .models import EmailTemplate
from django_tables2 import A

class EmailTable(tables.Table):
    subject = tables.TemplateColumn(
            '<a href="#modal-contents" class="modal-trigger" value="{{ record.id }}" name="{{ record.subject }}">{{ record.subject }}</a>',
            verbose_name='Onderwerp')
    to = tables.Column(verbose_name="Aan")
    cc = tables.Column(verbose_name="CC")
    bcc = tables.Column(verbose_name="BCC")
    sent_at = tables.Column(verbose_name="Verzonden op")


    class Meta:
        model = EmailTemplate
        fields = ('subject','to','cc','bcc', 'sent_at')
        attrs = {'class': 'striped responsive-table'}

class EmailTemplateTable(tables.Table):
    subject = tables.LinkColumn('edit_email_template', args=[A('pk')], verbose_name='Onderwerp')
    actions = tables.TemplateColumn(
        '<a href="{% url "edit_email_template" record.id %}"><i class="material-icons">edit</i></a><a href="#modal1" class="modal-trigger delete" value="{{ record.id }}" name="{{ record.title }}"><i class="material-icons">delete</i></a>',
        verbose_name='')

    class Meta:
        model = EmailTemplate
        fields = ('subject',)
        attrs = {'class': 'striped responsive-table'}
