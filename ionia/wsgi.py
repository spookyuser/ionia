"""
WSGI config for ionia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/

Modified from default to suit django-configurations:
https://django-configurations.readthedocs.io/en/stable/#quickstart
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ionia.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
