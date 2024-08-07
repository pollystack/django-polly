from django.urls import path
from .views import DashboardView

app_name = 'django_polly'  # This is important for namespacing

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # ... other URL patterns ...
]