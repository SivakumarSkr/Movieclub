
SECRET_KEY = 'gw8-*06vs1mei4=m-2_4m$5prx6=+l$&p5&rgo6mu$s02x8in@'

LOCAL_APPS = [
    'comments',
    'contents',
    'groups',
    # 'messaging',
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
]
THIRD_PARTY_APPS = [
    'django_extensions',
    'taggit',
    'markdownx',
]

INSTALLED_APPS = LOCAL_APPS + DEFAULT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'movieclub.urls'

WSGI_APPLICATION = 'movieclub.wsgi.application'
