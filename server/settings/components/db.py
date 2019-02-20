DATABASES_DEV = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hm',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASES_PROD = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd87nfbqvf8bdv9',
        'USER': 'xvzammcverouba',
        'PASSWORD': 'e194015546093749863526367a2ab3a3b9827c2e66fa94092025a0d958d4430d',
        'HOST': 'ec2-54-217-205-90.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}
