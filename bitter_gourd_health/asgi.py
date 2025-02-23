"""
ASGI config for bitter_gourd_health project.

This file configures the ASGI (Asynchronous Server Gateway Interface) for the bitter_gourd_health project.
ASGI serves as the interface between Django and asynchronous web servers and enables Django to handle asynchronous tasks, 
such as WebSockets or long-running background tasks.

The application is exposed as a module-level variable named `application`.

For more information, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os  # Standard library for interacting with operating system functionality
from django.core.asgi import get_asgi_application  # Django function to retrieve the ASGI application

# Sets the environment variable for the settings module to the main settings of the bitter_gourd_health project.
# This tells Django which settings to use for this application.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitter_gourd_health.settings')

# Creates the ASGI application instance using Django’s ASGI handler.
# This instance will be used by the ASGI server to communicate with Django.
application = get_asgi_application()
