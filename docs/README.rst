===========
django-polly
===========

`django-polly` is a Django application for managing Language Learning Models (LLMs) and facilitating AI-powered conversations within your Django project.

Features
--------

* LLM Management: Create and configure LLM instances (parrots)
* SmartConversations: Engage in AI-powered conversations
* WebSocket Support: Real-time communication for chat interfaces
* Admin Interface: Easily manage parrots and conversations
* Extensible: Designed to work with various LLM backends

Quick start
-----------

1. Install django-polly:

   .. code-block:: bash

       pip install django-polly

2. Add "django_polly" and its dependencies to your INSTALLED_APPS setting:

   .. code-block:: python

       INSTALLED_APPS = [
           ...
           'django_polly',
           'rest_framework',
           'django_json_widget',
       ]

3. Configure ASGI in your project's asgi.py:

   .. code-block:: python

       import os
       from django.core.asgi import get_asgi_application
       from channels.routing import ProtocolTypeRouter
       from django_polly.routing import polly_asgi_routes

       os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

       django_asgi_app = get_asgi_application()
       polly_asgi_routes["http"] = django_asgi_app

       application = ProtocolTypeRouter(polly_asgi_routes)

4. Update your settings.py:

   .. code-block:: python

       ASGI_APPLICATION = 'your_project.asgi.application'

       CHANNEL_LAYERS = {
           'default': {
               'BACKEND': 'channels.layers.InMemoryChannelLayer'
           }
       }

       AI_MODELS_PATH = os.path.join(BASE_DIR, "ai_models")

5. Include the django-polly URLconf in your project urls.py:

   .. code-block:: python

       path('polly/', include('django_polly.urls')),

6. Run migrations to create the django-polly models:

   .. code-block:: bash

       python manage.py migrate

7. Download a model:

   .. code-block:: bash

       python manage.py download_model "Qwen2-500M-Instruct-Q8_0.gguf" "https://huggingface.co/lmstudio-community/Qwen2-500M-Instruct-GGUF/resolve/main/Qwen2-500M-Instruct-Q8_0.gguf"

8. Start the development server:

   .. code-block:: bash

       python manage.py runserver

9. Visit http://127.0.0.1:8000/admin/ to create parrots (you'll need the Admin app enabled).

10. Visit http://127.0.0.1:8000/polly/ to start using django-polly.

Configuration
-------------

For detailed configuration options, please refer to the full documentation.

Documentation
-------------

The full documentation is at https://django-polly.readthedocs.io.

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: oss@pollystack.com

License
-------

The project is licensed under the AGPL-3.0 license.