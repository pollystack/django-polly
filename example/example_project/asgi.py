"""
ASGI config for example_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application
from django_polly.asgi_helpers import get_asgi_application as get_polly_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example_project.settings')

django_asgi_app = get_asgi_application()
application = get_polly_asgi_application(django_asgi_app)
