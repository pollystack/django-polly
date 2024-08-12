Introduction
============

Welcome to Django Polly!

Django Polly is a powerful extension for Django that brings the capabilities of Language Learning Models (LLMs) to your web applications. It provides a seamless way to integrate AI-powered conversations, content generation, and more into your Django projects.

Core Concepts
-------------

Parrots (LLMs)
^^^^^^^^^^^^^^

In Django Polly, we refer to our AI models as "Parrots". Each Parrot represents an instance of an LLM, with its own characteristics and capabilities.

SmartConversations
^^^^^^^^^^^^^^^^^^

SmartConversations are the heart of Django Polly. They represent an ongoing dialogue between a user and a Parrot, allowing for dynamic, AI-powered interactions.

LLM API
^^^^^^^

The LLM API is the bridge between your Django application and the underlying LLM. It handles the communication with the AI models, ensuring efficient and effective interactions.

Consumers
^^^^^^^^^

Django Polly uses Channels-style consumers to handle WebSocket connections, enabling real-time communication between users and Parrots.

How It Works
------------

1. Set up Parrots through Django's admin interface or programmatically.
2. Create SmartConversations to initiate dialogues between users and Parrots.
3. Use the LLM API to send messages and receive responses.
4. Optionally, use WebSocket consumers for real-time chat capabilities.

Django Polly takes care of the complexities of LLM integration, allowing you to focus on building engaging AI-powered features for your users.

Next Steps
----------

To get started with Django Polly, proceed to the :doc:`installation` guide, followed by our :doc:`tutorial/index` for a hands-on introduction to building with Django Polly.