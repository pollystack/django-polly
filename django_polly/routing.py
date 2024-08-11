from django.urls import path

from django_polly import consumers_local_demo
from smart_chat import (
    consumers_smart_gpt,
)

# from smart_chat import consumers_local_demo

websocket_urlpatterns = [
    # Demo WebSocket URL, disabled by default
    path(
        "ws/chatgpt-demo/",
        consumers_local_demo.ChatConsumerDemo.as_asgi(),
        name="chatgpt_demo",
    ),
    # New WebSocket URL for smart-gpt
    path(
        "ws/smart-gpt/<int:conversation_id>/",
        consumers_smart_gpt.SmartGPTConsumer.as_asgi(),  # Use your actual consumer class
        name="smart_gpt",
    ),
]
