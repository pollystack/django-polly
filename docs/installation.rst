Installation
------------

1. Install django-polly and its dependencies:

   .. code-block:: bash

       pip install django-polly

2. Add "django_polly" and its dependencies to your INSTALLED_APPS setting in settings.py:

   .. code-block:: python

       INSTALLED_APPS = [
           'daphne',  # Add this before all django apps
           'django.contrib.admin',
           'django.contrib.auth',
           'django.contrib.contenttypes',
           'django.contrib.sessions',
           'django.contrib.messages',
           'django.contrib.staticfiles',
           'django_polly',  # Add this after all django apps
           'rest_framework', # Required for API views
           'django_json_widget', # Required for JSON widget in admin (optional)
           # ... your other apps ...
       ]

3. Configure ASGI in your project's asgi.py:

   .. code-block:: python

       import os
       from django.core.asgi import get_asgi_application
       from channels.routing import ProtocolTypeRouter
       from django_polly.routing import polly_asgi_routes

       os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

       # Get the Django ASGI application
       django_asgi_app = get_asgi_application()

       # Use the Django ASGI application for HTTP requests
       polly_asgi_routes["http"] = django_asgi_app

       # Create the final ASGI application
       application = ProtocolTypeRouter(polly_asgi_routes)

4. Update your settings.py with the following:

   .. code-block:: python

       # Add this to specify the ASGI application
       ASGI_APPLICATION = 'your_project.asgi.application'
       WSGI_APPLICATION = 'your_project.wsgi.application'

       # Add this to for daphne
       CHANNEL_LAYERS = {
           'default': {
               'BACKEND': 'channels.layers.InMemoryChannelLayer'
           }
       }

       AI_MODELS_PATH = BASE_DIR / 'ai_models' # Add this to specify the path to store AI models

5. Include the django-polly URLconf in your project urls.py:

   .. code-block:: python

       from django.contrib import admin
       from django.urls import path, include

       urlpatterns += [
           path('admin/', admin.site.urls),
           path('polly/', include('django_polly.urls')),
           # ... other URL patterns ...
       ]

6. Run migrations:

   .. code-block:: bash

       python manage.py migrate

7. Download an AI model (example using Qwen2):

   .. code-block:: bash

       python manage.py download_model "Qwen2-500M-Instruct-Q8_0.gguf" "https://huggingface.co/lmstudio-community/Qwen2-500M-Instruct-GGUF/resolve/main/Qwen2-500M-Instruct-Q8_0.gguf"

8. Start the development server:

   .. code-block:: bash

       python manage.py runserver

   Visit http://127.0.0.1:8000/admin/ to create parrots and http://127.0.0.1:8000/polly/ to use django-polly.