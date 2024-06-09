"""
Django settings for projectmanager project.

Generated by 'django-admin startproject' using Django 4.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-gn@v&vp8svr02@j2q3l$0q$3jm=2w$i8ajn4zmdd!mzt#x_8$w"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# ALLOWED_HOSTS = ["*"]

#### For Render SetUp
# DEBUG = os.environ.get("DEBUG", "False").lower() == "True"
DEBUG = True
ALLOWED_HOSTS = ["*"]
# SECRET_KEY = os.environ.get("SECRET_KEY")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "projectdatabase",
    "channels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]



ROOT_URLCONF = "projectmanager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR,"templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "projectmanager.wsgi.application"

ASGI_APPLICATION = 'projectmanager.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


###### LOCAL POSTGRESQL DATABASE #########################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'projectData',
        "USER": 'postgres',
        "PASSWORD": '2024',
        "HOST": 'localhost'
    }
}

####### RENDER -POSTGRESQL CONNECTION ###################### 
'''for this install -- > pip install dj-database-url ✅
    NOT THIS -------> pip install dj_database_url ❌'''


renderDatabase = "postgres://shovan:22PXn8XwGmfmxZpMDqfVt5XrlIMumxtq@dpg-cpdc3v7sc6pc738rbc10-a.oregon-postgres.render.com/pmdb_thpj"
# postgres://shovan:22PXn8XwGmfmxZpMDqfVt5XrlIMumxtq@dpg-cpdc3v7sc6pc738rbc10-a.oregon-postgres.render.com/pmdb_thpj
# postgres://shovan:22PXn8XwGmfmxZpMDqfVt5XrlIMumxtq@dpg-cpdc3v7sc6pc738rbc10-a/pmdb_thpj
import dj_database_url

DATABASES["default"] = dj_database_url.parse(renderDatabase)

# DATABASES["default"] = dj_database_url.parse(os.environ.get("DATABASE_URL"))



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/




STATIC_URL = '/static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term
    #  caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'build', 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# import env

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': env('CLOUD_NAME'),
#     'API_KEY': env('CLOUD_API_KEY'),
#     'API_SECRET': env('CLOUD_API_SECRET')
# }

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dybf6f8gq',
    'API_KEY': '347962827317641',
    'API_SECRET': 'dLzewnRieWlbfD47MjiR1sA-hZ0'
}