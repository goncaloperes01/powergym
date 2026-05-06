import os
from pathlib import Path
import dj_database_url # Adiciona isto

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-YOUR_SECRET_KEY_HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'ginasio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ginasio_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ginasio_project.wsgi.application'

# LIGAÇÃO AO POSTGRESQL CORRIGIDA
# A tua nova configuração de Base de Dados
DATABASES = {
    'default': dj_database_url.config(
        # COLA AQUI O TEU LINK DO NEON.TECH (ENTRE AS ASPAS)
        default='postgresql://neondb_owner:npg_gRhyINn8k3Xt@ep-floral-band-ab9knw9i-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Ficheiros Estáticos (CSS/JS)
STATIC_URL = '/static/'  # <- Adicionada a barra no início
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # <- Linha Nova

# Pasta das Imagens (Media)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURAÇÕES DE LOGIN / LOGOUT ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'redirecionar_login' # Vai chamar a nossa inteligência
LOGOUT_REDIRECT_URL = 'login'

import os # Garante que tens este import lá no topo do ficheiro, se não tiveres, podes pôr aqui

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuração do Cloudinary (Fotos)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dfoqhtuci',
    'API_KEY': '853932941335875',
    'API_SECRET': 'CvquxV9CQxTtT91QuPPik1z2CgQ',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'