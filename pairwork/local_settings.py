LOCAL_SETTINGS = True
from settings import *
from django.utils.translation import ugettext_lazy as _
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(ROOT_PATH, '..', 'db', 'pairwork.sqlite3'),
    'USER': 'root',
    'PASSWORD': 'root',
    'HOST': 'localhost',
    'PORT': '3306',
}
LANGUAGES = (
    ('zh-cn',(_('Simplified Chinese'))),
    ('en',(_('English'))),
)

SITE = {
    'title': _('This is test title'), 
}

# redirect url after login
LOGIN_REDIRECT_URL = '/'

# Email use gmail currently
ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'workpair@gmail.com'
EMAIL_HOST_PASSWORD = 'workpair.pass'
EMAIL_PORT = 587

