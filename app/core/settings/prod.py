from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get("DEBUG", 0)
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["locahost", "callme.buh-ua.com.ua"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = u"Техподдержка БухгалтерияUA<mail@buh-ua.com.ua>"

EMAIL_HOST = "mail.buh-ua.com.ua"
EMAIL_HOST_USER = "mail@buh-ua.com.ua"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = 465
EMAIL_USE_TLS = True

SECURE_SSL_REDIRECT = True

# TODO: add this to env, 2 for dev version
SITE_ID = int(os.environ.get("SITE_ID", default=1))

STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")
STATIC_URL = "/public/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "public", "media")
MEDIA_URL = "/public/media/"

try:
    from .local import *
except ImportError:
    pass
