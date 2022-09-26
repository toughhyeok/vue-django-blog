from app.config.settings.base import *


DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASS'),
        'HOST': get_secret('DB_HOST')
    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = "/var/www/share-blog/static/"
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')