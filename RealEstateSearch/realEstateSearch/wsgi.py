"""
WSGI config for realEstateSearch project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

#settings_path = '/home/RealEstateSearch/realestatesearch.pythonanywhere.com'
#sys.path.insert(0, settings_path)

# Konfiguracja.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realEstateSearch.settings')

application = get_wsgi_application()
