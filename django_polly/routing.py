import os

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django_polly.urls import websocket_urlpatterns

polly_asgi_routes = {
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns,
            )
        )
    ),
}
