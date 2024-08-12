Installation
============

This guide will walk you through the process of installing Django Polly and setting it up in your Django project.

Requirements
------------

Django Polly requires:

* Python 3.8 or higher
* Django 3.2 or higher
* Channels 3.0 or higher

Installing Django Polly
-----------------------

1. Install Django Polly using pip:

   .. code-block:: bash

      pip install django-polly

2. Add 'django_polly' to your INSTALLED_APPS in your Django settings file:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'django_polly',
          'channels',
          ...
      ]

3. Set up the AI_MODELS_PATH in your settings:

   .. code-block:: python

      AI_MODELS_PATH = BASE_DIR / 'ai_models'

4. Configure ASGI in your project's asgi.py file:

   .. code-block:: python

      import os
      from django.core.asgi import get_asgi_application
      from channels.routing import ProtocolTypeRouter
      from django_polly.routing import polly_asgi_routes

      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

      django_asgi_app = get_asgi_application()
      polly_asgi_routes["http"] = django_asgi_app

      application = ProtocolTypeRouter(polly_asgi_routes)

5. Add Django Polly URLs to your project's urls.py:

   .. code-block:: python

      from django.urls import path, include

      urlpatterns = [
          ...
          path('polly/', include('django_polly.urls')),
          ...
      ]

6. Run migrations to create the necessary database tables:

   .. code-block:: bash

      python manage.py migrate

Verifying Installation
----------------------

To verify that Django Polly is installed correctly, start your Django development server and navigate to the admin interface. You should see new sections for managing Parrots and SmartConversations.

Next Steps
----------

Now that you have Django Polly installed, you're ready to start building AI-powered features in your Django project. Check out our :doc:`tutorial/index` for a step-by-step guide on creating your first AI-powered application with Django Polly.