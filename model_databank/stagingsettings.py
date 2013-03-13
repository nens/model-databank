from model_databank.settings import *

DATABASES = {
    'default': {
        'NAME': 'model_databank',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'postgres',
        'PASSWORD': 'ybOQG2b6asezy1khHkGv',
        'HOST': 'nens-3di-db-01.nens.local',
        'PORT': '',
    },
}

UI_GAUGES_SITE_ID = ''
