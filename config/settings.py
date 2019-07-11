"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 2.1.9.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # プロジェクトのpath
PROJECT_NAME = os.path.basename(BASE_DIR) # プロジェクトの名前

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=zjgip(+y7x$z6sk-(n+u=0^8hkxkv$7!*0x0ip=*buld--v2c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # 開発時はTrue,商用提供時はFalse

ALLOWED_HOSTS = ['*'] # デバックモードがFalseの時に設定要


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'searchapp.apps.SearchappConfig', #アプリ紐付け
    'bootstrap4' #bootstrap4紐付け
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # テンプレート探索優先ディレクトリ
        'APP_DIRS': True, # アプリ名フォルダ直下探索有無
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'protodb',
        'USER': 'root',
        'PASSWORD': 'rootpassword', # ローカル端末にインストールしたときのパスワード
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True, # トランザクションの有効範囲をリクエストの開始から終了までに設定
        'OPTIONS': {
            'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO', # 桁溢れの登録時にエラー（厳密モード）
            },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# デバックモードがFalseの時に有効化
STATIC_URL = '/static/' # 静的ファイルの配信用ディレクトリ
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # 静的ファイルの置き場所
STATIC_ROOT = '/var/www/{}/static' .format(PROJECT_NAME) # 静的ファイルの配信元

# セッションの設定
SESSION_COOKIE_AGE = 600 # 10分
SESSION_SAVE_EVERY_REQUEST = True # 1リクエストごとにセッション情報更新

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}