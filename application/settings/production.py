import os

from .defaults import *


DEBUG = False
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if host.strip()]

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT')
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT')

