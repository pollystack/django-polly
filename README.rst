Django Polly
============

.. image:: https://img.shields.io/pypi/v/django-polly.svg
    :target: https://pypi.python.org/pypi/django-polly

.. image:: https://img.shields.io/pypi/l/django-polly.svg
    :target: https://pypi.python.org/pypi/django-polly

.. image:: https://img.shields.io/pypi/pyversions/django-polly.svg
    :target: https://pypi.python.org/pypi/django-polly

.. image:: https://readthedocs.org/projects/django-polly/badge/?version=latest
    :target: https://django-polly.readthedocs.io/en/latest/?badge=latest

Django Polly enhances Django with Language Learning Model (LLM) capabilities, enabling AI-powered conversations, task automation, and other intelligent features in your Django projects. It uses familiar Django patterns and provides a flexible framework for customizing AI behaviors and supporting various LLM backends.

Features
--------

* LLM Management: Create and configure LLM instances (parrots)
* SmartConversations: Engage in AI-powered conversations
* WebSocket Support: Real-time communication for chat interfaces
* Admin Interface: Easily manage parrots and conversations
* Extensible: Designed to work with various LLM backends

Documentation, installation, and getting started instructions are at
https://django-polly.readthedocs.io

Quick Start
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

6. Run migrations and download a model:

   .. code-block:: bash

       python manage.py migrate
       python manage.py download_model "Qwen2-500M-Instruct-Q8_0.gguf" "https://huggingface.co/lmstudio-community/Qwen2-500M-Instruct-GGUF/resolve/main/Qwen2-500M-Instruct-Q8_0.gguf"

7. Start the development server and begin using django-polly:

   .. code-block:: bash

       python manage.py runserver

   Visit http://127.0.0.1:8000/admin/ to create parrots and http://127.0.0.1:8000/polly/ to use django-polly.

Dependencies
------------

Django Polly supports Python 3.8 and up, and is compatible with Django 4.2 and 5.0.

Contributing
------------

To learn more about contributing, please read our `contributing docs <https://django-polly.readthedocs.io/en/latest/contributing.html>`_.

Support
-------

If you're having issues, please let us know by opening an issue on our `GitHub repository <https://github.com/pollystack/django-polly/issues>`_.

For larger discussions, join our `mailing list <mailto:oss@pollystack.com>`_.

Maintenance and Security
------------------------

To report security issues, please contact security@pollystack.com. For more information on our security process, see our documentation.

Maintenance is overseen by the Pollystack team. We operate on a best-effort basis and prioritize security issues.

License
-------

The project is licensed under the AGPL-3.0 license.