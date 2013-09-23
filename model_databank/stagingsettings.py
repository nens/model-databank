from model_databank.testsettings import *

DATABASES = {
    'default': {
        'NAME': 'model_databank',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'threedi',
        'PASSWORD': 'klsdhadkjw',
        'HOST': 'nens-3di-db-01.nens.local',
        'PORT': '',
    },
}

UI_GAUGES_SITE_ID = ''
