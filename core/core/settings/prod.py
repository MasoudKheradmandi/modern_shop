from .base import *

from decouple import config


ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="*",
)
SECRET_KEY = config("SECRET_KEY", default="test")

DEBUG = config("DEBUG", cast=bool, default=False)

CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", cast=bool, default=False)
CSRF_USE_SESSIONS = config("CSRF_USE_SESSIONS", cast=bool, default=False)
CSRF_COOKIE_DOMAIN = config("CSRF_USE_SESSIONS",default='*')

MERCHANTID = config("MerchantID",default="test")
