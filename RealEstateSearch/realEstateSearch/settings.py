"""
Django settings for realEstateSearch project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# my configuration

API_URL = 'http://127.0.0.1:8000/api/searchingSettingsApi/'
API_OLXSEARCH_URL = 'http://127.0.0.1:8000/api/olxSearch/'
SCRAPING_URL_DEFAULT = f"""https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/ruda-slaska/?search%5bfilter_enum_rooms%5d%5b0%5d=one&search%5bfilter_float_price_per_m:to%5d=4000"""
SCRAPING_URL_PARAM_DEFAULT = {'city':'ruda-slaska', 'category': 'mieszkania', 'rooms':1, 'price':4000}


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', "asdfasdfa35qw4l*je+m&ys5dv#zoy)0a2+x1!m8hx290_sx&0gh")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', default=1)))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1').split(' ')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simpleRe': {
            'format': "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    'handlers': {
        'file_celery': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/celeryInfo.log',
            'formatter': 'simpleRe'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/info.log',
            'formatter': 'simpleRe',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/debug.log',
            'formatter': 'simpleRe',
        },
 
    },
    'loggers': {
        'django': {
            'handlers': ['file_info', 'file_debug'],
            'level': 'DEBUG',
            'propagate': True
        },
        'celeryLogger': {
            'handlers': ['file_celery'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    # my apps
    'olxSearch.apps.OlxSearchConfig',
    'scrapingApp.apps.ScrapingappConfig',
    ]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'realEstateSearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'olxSearch/templates'),
            os.path.join(BASE_DIR, 'templates/registration/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'realEstateSearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_LION = True     # orginalnie tego nie ma // dzięki temu admin będzie po polsku

USE_TZ = False      # orginalnie True

LOGIN_REDIRECT_URL = 'dashboard'        # nowe do logowania z wbudowanych widoków
LOGIN_URL = 'login'                     # nazwy wzorców url podanych w urls path
LOGOUT_URL = 'logout'                   # można również na sztywno wpisać adres url



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'    # drukuje maile do konsoli

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# celery broker and result
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://localhost:6379/0")

# email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('ENV_EMAIL_HOST','smtp.gmail.com')
EMAIL_HOST_USER = os.environ.get('ENV_EMAIL_HOST_USER','your_mail@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('ENV_EMAIL_HOST_PASSWORD',  'your_code')
EMAIL_PORT = os.environ.get('ENV_EMAIL_PORT' ,587)
EMAIL_USE_TLS = bool(int(os.environ.get('ENV_EMAIL_USE_TLS', default=1)))
EMAIL_USE_SSL = bool(int(os.environ.get('ENV_EMAIL_USE_SSL', default=0)))
DEFAULT_FROM_EMAIL = os.environ.get("ENV_DEFAULT_FROM_EMAIL","Welcome to Real Estate Search. Contact us at <your_mail@gmail.com> if you don't want receved emails")
