from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polly/', include('django_polly.urls')),  # This line is important
    # ... other URL patterns ...
]