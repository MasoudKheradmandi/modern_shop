from .base import *
from pathlib import Path
import sys


ALLOWED_HOSTS = []
DEBUG = True
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

# DATABASES = {
#     'default':
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     },
# }
