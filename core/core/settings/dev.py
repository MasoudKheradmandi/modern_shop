from pathlib import Path
import sys
from decouple import config

from .base import *
DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

import socket  # only if you haven't already imported this
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

ALLOWED_HOSTS = []
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-ljt_%&%yy93!^b27+ev+nx*c_pboq%)lx)&xhml60)3ga!46+s'

if sys.argv[1:2] == ['test']:
    ALLOWED_HOSTS = ['*']
    DEBUG = False
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.memory.InMemoryStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
MERCHANTID = config("MerchantID",default="test")
# DATABASES = {
#     'default':{
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     },
# }
