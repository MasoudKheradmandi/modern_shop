from .base import *

from decouple import config


ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="*",
)
SECRET_KEY = config("SECRET_KEY", default="test")

DEBUG = config("DEBUG", cast=bool, default=True)

MERCHANTID = config("MerchantID",default="test")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/",
        "KEY_PREFIX": "html_",
        "TIMEOUT": 60 * 15,  # in seconds: 60 * 15 (15 minutes)
    }
}