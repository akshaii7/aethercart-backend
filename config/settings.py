import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-^&brqp(m)=nx5n8uv)=b(i0gyn&#7ho2w0_0q6s697oait(ftr'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ==========================================
# ALLOWED HOSTS CONFIGURATION
# ==========================================
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = [
        'aethercart-backend.onrender.com',
        'localhost',
        '127.0.0.1',
        '*',
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'django_filters',
    'corsheaders',
    
    # Project Local apps
    'apps.accounts',
    'apps.cart',
    'apps.reviews',
    'apps.products',
    'apps.orders',
    'apps.delivery',
    'apps.payments',
    'apps.notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ഇത് മുകളിൽ തന്നെ കിടക്കണം
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (uploaded images)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Third Party Integrations

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_SrvHdRirv4LWsv")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "acDvBPxOCbwreZaU12TN5IdO")

# ==========================================
# CORS & CSRF SETTINGS FOR ANTIGRAVITY / LOGIN FIX
# ==========================================
CORS_ALLOW_ALL_ORIGINS = True  # ടെസ്റ്റിംഗിനും കണക്ഷൻ എറർ പൂർണ്ണമായി മാറാനും ഇത് സഹായിക്കും
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://aethercart-frontend.vercel.app",  # നിങ്ങളുടെ ലൈവ് Vercel ഫ്രണ്ട്എൻഡ് ലിങ്ക്
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
]

# 403 Forbidden എറർ പരിഹരിക്കാൻ ഇത് നിർബന്ധമാണ്
CSRF_TRUSTED_ORIGINS = [
    "https://aethercart-frontend.vercel.app",
    "https://aethercart-backend.onrender.com",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

# ==========================================
# SESSION & COOKIE SETTINGS FOR DJANGO ADMIN
# ==========================================
SESSION_COOKIE_AGE = 1209600  
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  
SESSION_SAVE_EVERY_REQUEST = True

# ==========================================
# JWT TOKEN SETTINGS FOR FRONTEND AUTO-LOGOUT FIX
# ==========================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),      # Token remains active for 1 day
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Login persistence lasts for 7 days
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}