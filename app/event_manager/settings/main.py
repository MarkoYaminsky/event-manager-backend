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
