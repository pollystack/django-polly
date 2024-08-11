
from django.urls import path
from django_polly import views, consumers, consumers_admin
from django_polly.views import DashboardView

app_name = 'django_polly'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('smart-gpt-chat/', views.chat, name='smart_gpt_chat'),
]

websocket_urlpatterns = [
    # Demo WebSocket URL, disabled by default
    path(
        "ws/smart-gpt-admin/",
        consumers_admin.SmartGPTConsumerAdmin.as_asgi(),
        name="smart_gpt_admin",
    ),
    # New WebSocket URL for smart-gpt
    path(
        "ws/smart-gpt/<int:conversation_id>/",
        consumers.SmartGPTConsumer.as_asgi(),  # Use your actual consumer class
        name="smart_gpt",
    ),
]