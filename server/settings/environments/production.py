import os
from server.settings.utils.utils import parse_db_variable

SECRET_KEY = os.environ.get('SECRET_KEY', 'SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['herokuapp.com']

db_variables = parse_db_variable(os.environ.get('DATABASE_URL'))
# use dev db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_variables[4],
        'USER': db_variables[0],
        'PASSWORD': db_variables[1],
        'HOST': db_variables[2],
        'PORT': db_variables[3]
    }
}





