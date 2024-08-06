from django.urls import path
from . import views
from .views import DashboardView

app_name = 'django_polly'

urlpatterns = [
    path('', views.parrot_list, name='parrot_list'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]