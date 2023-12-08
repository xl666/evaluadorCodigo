import environ
import os
from sistema_evaluacion_codigo.base import *

env = environ.Env()
env_file = os.path.join(BASE_DIR, '.env')
environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY_DEVELOPMENT")
DEBUG = True
SESSION_COOKIE_HTTPONLY = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME', 'evalcod'),
        'USER': os.environ.get('DATABASE_USER', 'Buzz'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'TingaDePollo953'),
        'HOST': os.environ.get('DATABASE_HOST', 'bd'),
        'PORT': os.environ.get('DATABASE_PORT', '3306'),
    }
}

