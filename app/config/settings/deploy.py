from app.config.settings.base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = "/var/www/share-blog/static/"
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')