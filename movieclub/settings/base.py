import os

import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = env("SECRET_KEY")

LOCAL_APPS = [
    'comments',
    'contents',
    'groups',
    'messaging',
    'notifications',
    'persons',
    'topics',
    'users',
    'suggestions',
    'shares',
    'movies',
]
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
]
THIRD_PARTY_APPS = [
    'django_extensions',
    'taggit',
    'markdownx',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'taggit_serializer',
    'generic_relations',
    'rest_framework_swagger',
    'corsheaders',
]

INSTALLED_APPS = LOCAL_APPS + DEFAULT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'movieclub.urls'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser", ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES':
        ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),

}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    # 'SECURITY_DEFINITIONS': {
    #     'api_key': {
    #         'type': 'apiKey',
    #         'in': 'header',
    #         'name': 'Authorization'
    #     }
    # }

}
SIMPLE_JWT = {
    'USER_ID_FIELD': 'pk'
}
