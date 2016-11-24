import django_tables2 as tables
from .models import EmailTemplate
from django_tables2 import A

class EmailTemplateTable(tables.Table):
    subject = tables.LinkColumn('edit_email_template', args=[A('pk')], verbose_name='Onderwerp')

    class Meta:
        model = EmailTemplate
        fields = ('subject',)
        attrs = {'class': 'striped responsive-table'}
