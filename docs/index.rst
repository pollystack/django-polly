Django Polly
============

Django Polly is a project that extends Django's capabilities to integrate Language Learning Models (LLMs) into your web applications. It provides a robust framework for managing AI models, conducting smart conversations, and leveraging AI capabilities within your Django projects.

Django Polly builds upon Django's powerful web framework, adding seamless LLM integration. It allows you to create, manage, and interact with AI models (which we call "Parrots") in both synchronous and asynchronous styles.

To get started with Django Polly, read our :doc:`introduction`, which will walk you through how things work.

.. note::
   This is documentation for the **0.0.1 series** of Django Polly. As this is a new project, be sure to check for updates regularly.

Projects
--------

Django Polly is comprised of several components:

* `Django Polly <https://github.com/pollystack/django-polly/>`_, the main Django integration layer
* `LLM API <https://github.com/pollystack/django-polly/blob/main/django_polly/lib/llm_api.py>`_, the core LLM interaction library
* `Channels Integration <https://github.com/pollystack/django-polly/blob/main/django_polly/consumers.py>`_, for real-time communication

This documentation covers the system as a whole; individual release notes and instructions can be found in the repository.

.. _topics:

Topics
------

.. toctree::
   :maxdepth: 2

   introduction
   installation
   tutorial/index
   topics/consumers
   topics/routing
   topics/models
   deploying
   topics/troubleshooting

Reference
---------

.. toctree::
   :maxdepth: 2

   api_reference
   models
   settings
   community
   contributing
   support
   releases/index