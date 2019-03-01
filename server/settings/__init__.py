from os import environ

from split_settings.tools import optional, include


# Managing environment via DJANGO_ENV variable:
environ.setdefault('DJANGO_ENV', 'production')
ENV = environ['DJANGO_ENV']

base_settings = [
    'components/common.py',
    'components/logging.py',
    'components/rest.py',
    'components/csp.py',
    'components/db.py',

    # You can even use glob:
    # 'components/*.py'

    # Select the right env:
    'environments/{0}.py'.format(ENV),

    # Optionally override some settings:
    optional('environments/local.py'),
]

# Include settings:
include(*base_settings)