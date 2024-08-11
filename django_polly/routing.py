from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django_polly.consumers import SmartGPTConsumer
from django_polly.consumers_admin import SmartGPTConsumerAdmin

websocket_urlpatterns = [
    path('polly/ws/smart-gpt-admin/', SmartGPTConsumerAdmin.as_asgi(), name="smart_gpt_admin"),
    path('polly/ws/smart-gpt/<int:conversation_id>/', SmartGPTConsumer.as_asgi(), name="smart_gpt"),
]

polly_asgi_routes = {
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
}