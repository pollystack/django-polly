from django.urls import path
from django_polly import views
from django_polly import consumers
from django_polly.views import DashboardView

app_name = 'django_polly'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('smart-gpt-chat/', views.smart_gpt_chat, name='chat'),
]

websocket_urlpatterns = [
    path('ws/smart-gpt/<int:conversation_id>/', consumers.SmartGPTConsumer.as_asgi(), name='smart_gpt'),
]
