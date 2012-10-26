import sys
import os

paths = ['/var/www/html/pairwork', '/var/www/html/pairwork/pairwork/apps']
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pairwork.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

