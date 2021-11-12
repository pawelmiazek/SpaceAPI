import logging
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

import environ


env = environ.Env()
root = environ.Path(__file__) - 2

BASE_DIR = root()
DEBUG = env("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
SITE_ID = env("SITE_ID", default=1)
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
EXTERNAL_API_URL = env.str(
    "EXTERNAL_API_URL", default="https://api.spacex.land/graphql/"
)

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "django_extensions",
    "auth_ex",
    "config",
    "cores",
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

# --- ADMIN ---
LOGIN_REDIRECT_URL = "/admin/"

# --- STATIC FILES ---
STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT", default="/project/static")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT", default="/project/media")

# --- TEMPLATES ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [root("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            )
        },
    }
]

# --- CORS ---
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ALLOW_ALL", default=False)
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])

# --- TIMEZONE ---
USE_TZ = True
TIME_ZONE = "UTC"

# --- LANGUAGES ---
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = "en-us"


LOCALE_PATHS = (root("locale"),)

# --- FILE UPLOAD ---
FILE_UPLOAD_MAX_MEMORY_SIZE = 2_621_440  # i.e. 2.5 MB
FILE_UPLOAD_PERMISSIONS = None
FILE_UPLOAD_DIRECTORY_PERMISSIONS = None

# --- DATABASE ---
DATABASES = {
    "default": env.db(default="postgres://postgres:postgres@postgres:5432/postgres")
}

AUTH_USER_MODEL = "auth_ex.User"

# --- REST FRAMEWORK ---
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "NON_FIELD_ERRORS_KEY": "errors",
    "DEFAULT_PAGINATION_CLASS": "config.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# --- AUTH ---
SIMPLE_JWT = {
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env("ACCESS_TOKEN_LIFETIME_MINUTES", default=30)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# ---- SWAGGER ----
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    "USE_SESSION_AUTH": False,
    "PERSIST_AUTH": True,
    "REFETCH_SCHEMA_WITH_AUTH": True,
    "REFETCH_SCHEMA_ON_LOGOUT": True,
}
