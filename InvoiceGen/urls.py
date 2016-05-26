from django.conf.urls import patterns, include, url
from django.contrib import admin
import FactuurMaker.views
import Magazine.views
import AgreementModule.views
# import RestApi.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', FactuurMaker.views.index, name='index'),
    url(r'^accounts/login/$', FactuurMaker.views.user_login, name='user_login'),
    url(r'^logout/$', FactuurMaker.views.user_logout, name='logout'),
    url(r'^article/(?P<articleid>\d+)/(.*)$', FactuurMaker.views.view_article, name='view_article'),
    url(r'^article/add/$', FactuurMaker.views.add_article, name='add_article'),
    url(r'^article/edit/(?P<articleid>\d+)/$', FactuurMaker.views.edit_article, name='edit_article'),
    url(r'^article/delete/(?P<articleid>\d+)/$', FactuurMaker.views.delete_article, name='delete_article'),
    url(r'^generate/invoice/$', FactuurMaker.views.generate_invoice, name='generate_invoice'),
    url(r'^invoices/$', FactuurMaker.views.get_invoices, name='get_invoices'),
    url(r'^invoices/add/article/$', FactuurMaker.views.add_article_to_invoice, name='add_article_to_invoice'),
    url(r'^invoices/delete/article/$', FactuurMaker.views.delete_article_from_invoice, name='delete_article_from_invoice'),
    url(r'^invoice/add/$', FactuurMaker.views.add_invoice, name='add_invoice'),
    url(r'^invoice/edit/(?P<invoiceid>\d+)/$', FactuurMaker.views.edit_invoice, name='edit_invoice'),
    url(r'^invoice/delete/(?P<invoiceid>\d+)/$', FactuurMaker.views.delete_invoice, name='delete_invoice'),
    url(r'^markdown/(?P<invoice_id>\d+)/', FactuurMaker.views.view_markdown, name='view_markdown'),
    url(r'^download/md/(?P<invoice_id>\d+)/', FactuurMaker.views.download_markdown, name='download_markdown'),
    url(r'^settings/$', FactuurMaker.views.settings, name='settings'),
    url(r'^settings/user/(?P<userid>\d+)/company/(?P<companyid>\d+)$', FactuurMaker.views.settings, name='settings'),
    url(r'^statistics/$', FactuurMaker.views.view_statistics, name='statistics'),

    url(r'^agreements/$', AgreementModule.views.agreement_index,
        name='agreement_index'),
    url(r'^agreements/new-model-agreement/$', AgreementModule.views.add_agreement_text,
        name='add_agreement_text'),
    url(r'^agreements/new-agreement/$', AgreementModule.views.add_agreement,
        name='add_agreement'),
    url(r'^agreements/view-sign-agreement/(?P<url>\w+)$', AgreementModule.views.view_agreement,
        name='view_agreement'),

    # url(r'^data/articles/$', RestApi.views.get_json_article_list, name='get_json_article_list'),
    # url(r'^data/article/(?P<article_id>\d+)$', RestApi.views.get_json_article, name='get_json_article'),
    # url(r'^data/save/article/$', RestApi.views.save_json_article, name='save_json_article'),
    # url(r'^data/session_id/$', RestApi.views.get_session_id, name='get_session_id'),
    # url(r'^data/magazines/$', RestApi.views.get_json_magazine_list, name='get_json_magazine_list'),
    # url(r'^data/magazine/(?P<magazine_id>\d+)$', RestApi.views.get_json_magazine, name='get_json_magazine'),
]
