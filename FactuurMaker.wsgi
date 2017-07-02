import os
import sys
sys.path.append('/var/www/')
sys.path.append('/var/www/FactuurMaker')
os.environ['DJANGO_SETTINGS_MODULE'] = 'InvoiceGen.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
