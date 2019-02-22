from server.settings.components.db import DATABASES_DEV

SECRET_KEY = "my_awesome_secret_key"
DEBUG = True

ALLOWED_HOSTS = ['*']

# use dev db
DATABASES = DATABASES_DEV
