from django.urls import path
from . import views

app_name = 'django_polly'

urlpatterns = [
    path('', views.parrot_list, name='parrot_list'),
]