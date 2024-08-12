import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

from django_polly.routing import polly_asgi_routes

# Get the Django ASGI application
django_asgi_app = get_asgi_application()


# Use the Django ASGI application for HTTP requests
polly_asgi_routes["http"] = django_asgi_app

# Create the final ASGI application
application = ProtocolTypeRouter(polly_asgi_routes)
