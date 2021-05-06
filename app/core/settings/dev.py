from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "=-@2uihr6(e(m8(e7lpq0x*#n38(0n!cxt=dwurotq+of4lc(3"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECURE_SSL_REDIRECT = False

# TODO: add this to env, 2 for dev version
SITE_ID = int(os.environ.get("SITE_ID", default=1))

try:
    from .local import *
except ImportError:
    pass
