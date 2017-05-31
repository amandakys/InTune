from webapps34.settings import *

DEBUG = False
ALLOWED_HOSTS = ['146.169.45.104']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'g1627134_u',
        'USER': 'g1627134_u',
        'PASSWORD': 'KsXTjjAPrP',
        'HOST': 'db.doc.ic.ac.uk',
        'PORT': '5432',
    }
}
