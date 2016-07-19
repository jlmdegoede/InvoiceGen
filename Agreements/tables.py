import django_tables2 as tables
from .models import Agreement, AgreementText


class AgreementTextTable(tables.Table):
    title = tables.Column(verbose_name='Titel')
    actions = tables.TemplateColumn('<a href="{% url "edit_model_agreement" record.id %}"><i class="material-icons">edit</i></a><a href="#" class="modal-trigger delete" value="{{ record.id }}" name="{{ record.title }}"><i class="material-icons">delete</i></a>', verbose_name='')

    class Meta:
        model = AgreementText
        attrs = {'class':  'striped responsive-table'}
        fields = ('title',)


class AgreementTable(tables.Table):
    created = tables.TemplateColumn('<a href="{% url "view_agreement" record.url %}">{{ record.created }}</a>', verbose_name='Gemaakt op')
    article_concerned = tables.TemplateColumn("{% for product in record.article_concerned.all %}{{ product.title }}, {% endfor %}", verbose_name='Opdrachten')
    company = tables.Column(verbose_name='Opdrachtgever')
    signed_by_contractor = tables.BooleanColumn(verbose_name='Ondertekend')

    class Meta:
        model = Agreement
        attrs = {'class': 'striped responsive-table'}
        fields = ('created', 'article_concerned', 'company', 'signed_by_contractor')