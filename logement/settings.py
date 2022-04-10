"""
Django settings for logement project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import json
import os
import logement.startup

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from firebase_admin import initialize_app

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=str(BASE_DIR/"key.json")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lgvtx5is(8&nejfxxckybss-r!5hhbd7qc^gyhr#)wr-8k5^9d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.105', "localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portail',
    "fcm_django"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'logement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'logement.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOOKUP_URLS=[
    "https://www.blot-immobilier.fr/habitat/location/appartement--appartement-neuf/ille-et-vilaine/rennes/?t3=true&t4=true",
    "https://www.ouestfrance-immo.com/louer/appartement--3-pieces_4-pieces/?lieux=100003,100013&prix=0_950",
    "https://www.giboire.com/recherche-location/appartement/?address%5B%5D=RENNES&priceMin=500&priceMax=950&livingSurfaceMin=55&livingSurfaceMax=90&nbBedrooms%5B%5D=2&nbBedrooms%5B%5D=3&searchBy=undefined#both",
    "https://www.pigeaultimmobilier.com/location/?sous-categorie%5B%5D=1455&agences%5B%5D=26548&prix_min=500&prix_max=950&submitted=1&o=date-desc&action=load_search_results&wia_6_type=location&searchOnMap=0&wia_1_reference=",
    "https://www.bienici.com/realEstateAds.json?filters=%7B%22size%22%3A24%2C%22from%22%3A0%2C%22showAllModels%22%3Afalse%2C%22filterType%22%3A%22rent%22%2C%22propertyType%22%3A%5B%22flat%22%5D%2C%22minPrice%22%3A600%2C%22maxPrice%22%3A950%2C%22minRooms%22%3A3%2C%22maxRooms%22%3A4%2C%22minArea%22%3A55%2C%22maxArea%22%3A90%2C%22page%22%3A1%2C%22sortBy%22%3A%22relevance%22%2C%22sortOrder%22%3A%22desc%22%2C%22onTheMarket%22%3A%5Btrue%5D%2C%22zoneIdsByTypes%22%3A%7B%22zoneIds%22%3A%5B%22-54517%22%5D%7D%7D&extensionType=extendedIfNoResult",
    "https://www.cabinet-martin.fr/location/appartement/rennes/3-pieces--4-pieces/600-euros-minimum/950-euros-maximum",
]

CRITERES = {
    "loyer.min" : 550,
    "loyer.max" : 950,
    "surface.min" : 55,
    "surface.max" : 90,
    "words.include" : (BASE_DIR / "conf" / "include"),
    "words.exclude" : (BASE_DIR / "conf" / "exclude"),
    "score.min" : 0
}
EMAILS=[]

DOMAIN = "logement.gautrais.eu"

for k, v in json.loads((BASE_DIR / "conf/conf.json").read_text()).items():
    exec(f"{k} = {json.dumps(v)}")


DATA_PATH = BASE_DIR / "data"

if not DATA_PATH.is_dir():
    DATA_PATH.mkdir(parents=True)

CACHE_PATH = DATA_PATH / "cache"


if not CACHE_PATH.is_dir():
    CACHE_PATH.mkdir(parents=True)


PASSWORD_FILE = BASE_DIR / "conf/password"


PASSWORD = PASSWORD_FILE.read_text().split("\n")[0]
if not len(PASSWORD):
    print(f"Merci de rensigner le mot de passe dans {PASSWORD_FILE.resolve()}")
    exit(0)


FIREBASE_APP = initialize_app()
FCM_APIKEY = " AIzaSyAap-Z8-VkpcdbbTnRT3cPIZm9KtrJUdYM"
FCM_DJANGO_SETTINGS = {
     # default: _('FCM Django')
    "APP_VERBOSE_NAME": "Mon Application",
     # true if you want to have only one active device per registered user at a time
     # default: False
    "ONE_DEVICE_PER_USER": True,
     # devices to which notifications cannot be sent,
     # are deleted upon receiving error response from FCM
     # default: False
    "DELETE_INACTIVE_DEVICES": False,
    # Transform create of an existing Device (based on registration id) into
                # an update. See the section
    # "Update of device with duplicate registration ID" for more details.
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

STATICFILES_DIRS = [
    BASE_DIR / "www" / "static",
]

"""
"""