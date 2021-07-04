DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'SCIE',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '172.16.2.194',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'es'

MAIL_HOST = 'onei.gob.cu'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'sistema.cie@onei.gob.cu'

EMAIL_HOST_PASSWORD = 'P@$$onei2020'

DOMAIN = 'scie.onei.gob.cu'