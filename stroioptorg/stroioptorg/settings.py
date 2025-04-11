"""Django settings for stroioptorg project.Generated by 'django-admin startproject' using Django 5.1.4.For more information on this file, seehttps://docs.djangoproject.com/en/5.1/topics/settings/For the full list of settings and their values, seehttps://docs.djangoproject.com/en/5.1/ref/settings/"""import osfrom pathlib import Pathimport environenv = environ.Env(    DEBUG=(bool, False))# Build paths inside the project like this: BASE_DIR / 'subdir'.BASE_DIR = Path(__file__).resolve().parent.parentenv.read_env(os.path.join(BASE_DIR, '.env'), override=True)# Quick-start development settings - unsuitable for production# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/# SECURITY WARNING: keep the secret key used in production secret!SECRET_KEY = env('SECRET_KEY')# SECURITY WARNING: don't run with debug turned on in production!DEBUG = env('DEBUG')ALLOWED_HOSTS = ['*']INTERNAL_IPS = [    '127.0.0.1',  # Localhost    'localhost',  # Localhost alias]# Application definitionthird_party_apps = [    'rest_framework',    'drf_spectacular',    'debug_toolbar',    'silk']apps = [    'main',    'users',    'product',    'order',    'wishlist']INSTALLED_APPS = [    'django.contrib.admin',    'django.contrib.auth',    'django.contrib.contenttypes',    'django.contrib.sessions',    'django.contrib.messages',    'django.contrib.staticfiles',    *third_party_apps,    *apps]MIDDLEWARE = [    'django.middleware.security.SecurityMiddleware',    'django.contrib.sessions.middleware.SessionMiddleware',    'django.middleware.common.CommonMiddleware',    'django.middleware.csrf.CsrfViewMiddleware',    'django.contrib.auth.middleware.AuthenticationMiddleware',    'django.contrib.messages.middleware.MessageMiddleware',    'django.middleware.clickjacking.XFrameOptionsMiddleware',    # library    'debug_toolbar.middleware.DebugToolbarMiddleware',    'silk.middleware.SilkyMiddleware',        # custom    'product.middleware.SaveOldSessionKeyMiddleware']ROOT_URLCONF = 'stroioptorg.urls'TEMPLATES = [    {        'BACKEND': 'django.template.backends.django.DjangoTemplates',        'DIRS': [BASE_DIR / 'templates'],        'APP_DIRS': True,        'OPTIONS': {            'context_processors': [                'django.template.context_processors.debug',                'django.template.context_processors.request',                'django.contrib.auth.context_processors.auth',                'django.contrib.messages.context_processors.messages',            ],        },    },]WSGI_APPLICATION = 'stroioptorg.wsgi.application'# Database# https://docs.djangoproject.com/en/5.1/ref/settings/#databasesDATABASES = {    'default': {        'ENGINE': 'django.db.backends.sqlite3',        'NAME': BASE_DIR / 'db.sqlite3',    }}# Password validation# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validatorsAUTH_PASSWORD_VALIDATORS = [    {        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    },    {        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',    },    {        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',    },    {        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',    },]# Internationalization# https://docs.djangoproject.com/en/5.1/topics/i18n/LANGUAGE_CODE = 'ru'TIME_ZONE = 'UTC'USE_I18N = TrueUSE_TZ = True# Static files (CSS, JavaScript, Images)# https://docs.djangoproject.com/en/5.1/howto/static-files/STATIC_URL = 'static/'STATICFILES_DIRS = [BASE_DIR / 'static']STATIC_ROOT = 'staticfiles/'# media filesMEDIA_URL = '/media/'MEDIA_ROOT = BASE_DIR / 'media'# Default primary key field type# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-fieldAUTHENTICATION_BACKENDS = (    'django.contrib.auth.backends.ModelBackend',  # Используем стандартный бекенд)DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'AUTH_USER_MODEL = 'users.User'LOGIN_URL = "users:login"LOGIN_REDIRECT_URL = "main:home"LOGOUT_REDIRECT_URL = "main:home"# DRFREST_FRAMEWORK = {    'EXCEPTION_HANDLER': 'utils.exception_handler.drf_custom_exception_handler',    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',    'DEFAULT_AUTHENTICATION_CLASSES': [        'rest_framework.authentication.SessionAuthentication',  # Для входа через Django Admin        'rest_framework.authentication.TokenAuthentication',  # Для токенов DRF    ],}# drf spectacular settingsSPECTACULAR_SETTINGS = {    'TITLE': 'STROIOPTORG API',    'DESCRIPTION': 'STROIOPTORG is online building market',    'VERSION': '0.0.1',    'SERVE_INCLUDE_SCHEMA': False,    # OTHER SETTINGS    'SWAGGER_UI_SETTINGS': {        'persistAuthorization': True,  # Запоминать токен между перезагрузками страницы    },    'AUTHENTICATION_CLASSES': [        'rest_framework.authentication.SessionAuthentication',        'rest_framework.authentication.TokenAuthentication',    ],    'SessionAuth': {        'type': 'apiKey',        'in': 'cookie',        'name': 'sessionid',    },    'TokenAuth': {        'type': 'apiKey',        'in': 'header',        'name': 'Authorization',    },    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',}# Email settingsEMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'EMAIL_HOST = 'smtp.gmail.com'EMAIL_PORT = 587EMAIL_USE_TLS = TrueEMAIL_HOST_USER = env('EMAIL_HOST_USER')EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')DEFAULT_FROM_EMAIL = EMAIL_HOST_USER# Strip settingsSTRIPE_API_KEY = env('STRIPE_API_KEY')STRIPE_ENDPOINT_KEY = env('STRIPE_ENDPOINT_KEY')