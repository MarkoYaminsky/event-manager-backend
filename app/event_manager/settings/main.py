import os

from .base import *

SECRET_KEY = getenv("SECRET_KEY")

ALLOWED_HOSTS = ["localhost"]

WSGI_APPLICATION = "app.event_manager.wsgi.application"

USE_TZ = True

SPECTACULAR_SETTINGS = {
    "TITLE": "Event manager",
    "DESCRIPTION": "A project which goal is to help organize one's activities.",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CELERY_BROKER_URL = os.getenv("REDIS_SOCKET", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_SOCKET", "redis://redis:6379/0")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("GMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("GMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
