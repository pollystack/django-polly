from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django_polly.urls import websocket_urlpatterns


def get_asgi_application(http_handler):
    return ProtocolTypeRouter({
        "http": http_handler,
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    })
