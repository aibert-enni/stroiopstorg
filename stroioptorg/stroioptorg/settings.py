"""Django settings for stroioptorg project.Generated by 'django-admin startproject' using Django 5.1.4.For more information on this file, seehttps://docs.djangoproject.com/en/5.1/topics/settings/For the full list of settings and their values, seehttps://docs.djangoproject.com/en/5.1/ref/settings/"""import osfrom pathlib import Pathfrom dotenv import load_dotenvload_dotenv()# Build paths inside the project like this: BASE_DIR / 'subdir'.BASE_DIR = Path(__file__).resolve().parent.parent# Quick-start development settings - unsuitable for production# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/# SECURITY WARNING: keep the secret key used in production secret!SECRET_KEY = 'django-insecure-*^3a#q_ib4%*q6^h3ab4dnx8c9houo742^ndgwd1_y)$z5x7ki'# SECURITY WARNING: don't run with debug turned on in production!DEBUG = TrueALLOWED_HOSTS = ['*']INTERNAL_IPS = [    '127.0.0.1',  # Localhost    'localhost',   # Localhost alias]# Application definitionINSTALLED_APPS = [    'django.contrib.admin',    'django.contrib.auth',    'django.contrib.contenttypes',    'django.contrib.sessions',    'django.contrib.messages',    'django.contrib.staticfiles',    # third party library    'rest_framework',    'debug_toolbar',    # apps    'main',    'users',    'product']MIDDLEWARE = [    'django.middleware.security.SecurityMiddleware',    'django.contrib.sessions.middleware.SessionMiddleware',    'django.middleware.common.CommonMiddleware',    'django.middleware.csrf.CsrfViewMiddleware',    'django.contrib.auth.middleware.AuthenticationMiddleware',    'django.contrib.messages.middleware.MessageMiddleware',    'django.middleware.clickjacking.XFrameOptionsMiddleware',    # library    'debug_toolbar.middleware.DebugToolbarMiddleware']ROOT_URLCONF = 'stroioptorg.urls'TEMPLATES = [    {        'BACKEND': 'django.template.backends.django.DjangoTemplates',        'DIRS': [BASE_DIR / 'templates'],        'APP_DIRS': True,        'OPTIONS': {            'context_processors': [                'django.template.context_processors.debug',                'django.template.context_processors.request',                'django.contrib.auth.context_processors.auth',                'django.contrib.messages.context_processors.messages',            ],        },    },]WSGI_APPLICATION = 'stroioptorg.wsgi.application'# Database# https://docs.djangoproject.com/en/5.1/ref/settings/#databasesDATABASES = {    'default': {        'ENGINE': 'django.db.backends.sqlite3',        'NAME': BASE_DIR / 'db.sqlite3',    }}# Password validation# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validatorsAUTH_PASSWORD_VALIDATORS = [    {        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    },    {        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',    },    {        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',    },    {        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',    },]# Internationalization# https://docs.djangoproject.com/en/5.1/topics/i18n/LANGUAGE_CODE = 'ru'TIME_ZONE = 'UTC'USE_I18N = TrueUSE_TZ = True# Static files (CSS, JavaScript, Images)# https://docs.djangoproject.com/en/5.1/howto/static-files/STATIC_URL = 'static/'STATICFILES_DIRS = [BASE_DIR / 'static']# media filesMEDIA_URL = '/media/'MEDIA_ROOT = BASE_DIR / 'media'# Default primary key field type# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-fieldAUTHENTICATION_BACKENDS = (    'django.contrib.auth.backends.ModelBackend',  # Используем стандартный бекенд)DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'AUTH_USER_MODEL = 'users.User'LOGIN_URL = "users:login"LOGIN_REDIRECT_URL = "main:home"LOGOUT_REDIRECT_URL = "main:home"# Email settingsEMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'EMAIL_HOST = 'smtp.gmail.com'EMAIL_PORT = 587EMAIL_USE_TLS = TrueEMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')DEFAULT_FROM_EMAIL = EMAIL_HOST_USER