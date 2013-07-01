import os
from django.conf import global_settings

# Django settings for contributors project.

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJECT_PATH, "data")
CACHE_PATH = os.path.join(PROJECT_PATH, "lp_data/cache")

DEBUG = True
TEMPLATE_DEBUG = DEBUG
STATIC_SERVE = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'uploads.context_processor.user_context',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(PROJECT_PATH, "temp_data")
if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_openid_auth',
    'django.contrib.admin',
    'django.contrib.comments',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'uploads',
    'south'
)

# OpenID and Launchpad intigration
AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

OPENID_CREATE_USERS = True
LOGIN_URL = '/openid/login/'
LOGIN_REDIRECT_URL = '/'
OPENID_SSO_SERVER_URL = 'server-endpoint-url'
OPENID_SSO_SERVER_URL = 'https://login.ubuntu.com/'
OPENID_LAUNCHPAD_STAFF_TEAMS = ['ubuntu-developer-advisory-team']
OPENID_LAUNCHPAD_TEAMS_MAPPING_AUTO = True
OPENID_UPDATE_DETAILS_FROM_SREG = True
OPENID_USE_AS_ADMIN_LOGIN = True
OPENID_FOLLOW_RENAMES = True
OPENID_STRICT_USERNAMES = True
# Currently we allow DAT, CC, DMB to see everything. This could
# be extended at some point to give other teams (say Ubuntu Members)
# the ability to see anonymous data.
#
# Whn this is changed './manage.py create_user_groups'
# must be run.
ALLOWED_LAUNCHPAD_TEAMS = ['ubuntu-developer-advisory-team',
                           'developer-membership-board',
                           'communitycouncil',
                           'canonical-community',
                           'greenhouse']

AUTH_PROFILE_MODULE = "uploads.UserProfile"

DATABASE_ROUTERS = ['uploads.router.DBRouter']

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


DEBUG_APPS = ()
DEBUG_MIDDLEWARE_CLASSES = ()
try:
    from local_settings import *
    INSTALLED_APPS += DEBUG_APPS
    MIDDLEWARE_CLASSES += DEBUG_MIDDLEWARE_CLASSES
except ImportError:
    logging.warning("No local_settings.py were found. See INSTALL for instructions.")
