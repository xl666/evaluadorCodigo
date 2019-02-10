import environ

from sistema_evaluacion_codigo.base import *

env = environ.Env()
env_file = os.path.join(BASE_DIR, '.env')
environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY_PRODUCTION")
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST':  env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    }
}

