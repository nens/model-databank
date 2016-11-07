import os

# from lizard_ui.settingshelper import setup_logging
# from lizard_ui.settingshelper import STATICFILES_FINDERS

DEBUG = True
TEMPLATE_DEBUG = True

# SETTINGS_DIR allows media paths and so to be relative to this settings file
# instead of hardcoded to c:\only\on\my\computer.
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))

# BUILDOUT_DIR is for access to the "surrounding" buildout, for instance for
# BUILDOUT_DIR/var/static files to give django-staticfiles a proper place
# to place all collected static files.
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))
#LOGGING = setup_logging(BUILDOUT_DIR)


# ENGINE: 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# In case of geodatabase, prepend with:
# django.contrib.gis.db.backends.(postgis)
DATABASES = {
    # If you want to use another database, consider putting the database
    # settings in localsettings.py. Otherwise, if you change the settings in
    # the current file and commit them to the repository, other developers will
    # also use these settings whether they have that database or not.
    # One of those other developers is Jenkins, our continuous integration
    # solution. Jenkins can only run the tests of the current application when
    # the specified database exists. When the tests cannot run, Jenkins sees
    # that as an error.
    'default': {
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'sqlite', 'test.db'),
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # empty string for localhost.
        'PORT': '',  # empty string for default.
        }
    }
SITE_ID = 1
SECRET_KEY = 'This is not secret but that is ok.'
INSTALLED_APPS = [
    'model_databank',
    'staticfiles',
    'south',
    'django_nose',
    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.gis',
    'django.contrib.sites',
    'django.contrib.webdesign',
    'django.contrib.messages',

    'crispy_forms',
    'rest_framework',
]
ROOT_URLCONF = 'model_databank.urls'

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    ]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Used for django-staticfiles (and for media files
STATIC_URL = '/static_media/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'static')
MEDIA_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'media')
#STATICFILES_FINDERS = STATICFILES_FINDERS

HG_CMD = '/usr/local/bin/hg'

# from lizard_ui/settingshelper.py
STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder',
    # Enable 'old' /media directories in addition to /static.
    'staticfiles.finders.LegacyAppDirectoriesFinder',
    # Enable support for django-compressor.
    'compressor.finders.CompressorFinder',
)



# from lizard_ui/settingshelper.py
def setup_logging(buildout_dir,
                  console_level='DEBUG',
                  file_level='WARN',
                  sentry_level=None,
                  sql=False):
    """Return configuration dict for logging.

    Some keyword arguments can be used to configure the logging.

    - ``console_level='DEBUG'`` sets the console level. None means quiet.

    - ``file_level='WARN'`` sets the var/log/django.log level. None means
      quiet.

    - ``sentry_level=None`` sets the sentry level. None means sentry logging
        is removed from the logging.

    - ``sql=False`` switches sql statement logging on or off.

    """
    result = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s %(name)s %(levelname)s\n%(message)s',
                },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
                },
            'console': {
                'level': console_level,
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'logfile': {
                'level': file_level,
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(buildout_dir,
                                         'var', 'log', 'django.log'),
                },
            'sentry': {
                'level': sentry_level,
                'class': 'raven.contrib.django.handlers.SentryHandler',
                'formatter': 'verbose'
            },
            },
        'loggers': {
            '': {
                'handlers': [],
                'propagate': True,
                'level': 'DEBUG',
                },
            'django.db.backends': {
                'handlers': ['null'],  # Quiet by default!
                'propagate': False,
                'level': 'DEBUG',
                },
            },
        }
    if console_level is not None:
        result['loggers']['']['handlers'].append('console')
    if file_level is not None:
        result['loggers']['']['handlers'].append('logfile')
    if sentry_level is not None:
        result['loggers']['']['handlers'].append('sentry')
    else:
        # When sentry is still in the handlers sentry needs to be installed
        # which gave import errors in Django 1.4.
        del result['handlers']['sentry']
    if sql:
        result['loggers']['django.db.backends']['handlers'] = [
            'console', 'logfile']
    return result

LOGGING = setup_logging(BUILDOUT_DIR)

try:
    # Import local settings that aren't stored in svn/git.
    from model_databank.local_testsettings import *
except ImportError:
    pass
