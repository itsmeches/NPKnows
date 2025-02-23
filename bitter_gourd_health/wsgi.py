"""
WSGI config for bitter_gourd_health project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os  # Import the os module to interact with the operating system

from django.core.wsgi import get_wsgi_application  # Import Django's WSGI application handler

# Set the default settings module for the 'bitter_gourd_health' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitter_gourd_health.settings')

# Get the WSGI application for the project
application = get_wsgi_application()  # This prepares the WSGI application callable

