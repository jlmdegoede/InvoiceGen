import django_tables2 as tables
from .models import EmailTemplate
from django_tables2 import A

class EmailTable(tables.Table):
    subject = tables.LinkColumn('edit_email_template', args=[A('pk')], verbose_name='Onderwerp')
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

    class Meta:
        model = EmailTemplate
        fields = ('subject',)
        attrs = {'class': 'striped responsive-table'}
