
from django.urls import path
from django_polly import views, consumers, consumers_admin
from django_polly.views import DashboardView

app_name = 'django_polly'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('smart-gpt-chat/<int:conversation_id>/', views.smart_gpt_chat, name='smart_gpt_chat'),
]
