from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django_polly import routing


def get_asgi_application(http_handler):
    return ProtocolTypeRouter({
        "http": http_handler,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    })
