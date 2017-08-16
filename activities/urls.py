from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
import activities.views

urlpatterns = [
    url(r'^$', activities.views.index, name='activity_index'),
]

