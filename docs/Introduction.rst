Introduction
============

Welcome to django-polly!

django-polly is a Django application that brings the power of Language Learning Models (LLMs) to your Django project. It allows you to create, manage, and interact with AI models, enabling a wide range of AI-powered features in your web applications.

Core Concepts
-------------

Parrots (GPT) and SmartConversations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the heart of django-polly are two key models: Parrots and SmartConversations.

* **Parrot**: Represents an instance of an LLM. Each Parrot has attributes like name, color, age, and the specific LLM model it's using. Parrots are the AI entities that power your conversations.

* **SmartConversation**: Represents a conversation session. It's linked to a user and contains a series of messages. This is where the interaction between users and Parrots happens.

* **Message**: Represents individual messages within a SmartConversation. Each message has content and is associated with either the user or the AI assistant.

LLM API and Connectors
^^^^^^^^^^^^^^^^^^^^^^

django-polly provides a robust API for interacting with LLMs:

* **LLMConnect**: The main class for initializing and managing LLM connections. It handles model loading and provides a high-level interface for interacting with the AI.

* **LLMInvoker**: Responsible for sending messages to the LLM and streaming responses. It manages the conversation flow between the user and the AI.

* **LLMModelType**: An enumeration of supported LLM models, allowing easy selection and management of different AI models.

Consumers for Real-time Communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

django-polly leverages Django Channels to provide real-time communication:

* **SmartGPTConsumer**: An asynchronous WebSocket consumer that handles real-time chat interactions. It manages the flow of messages between the user and the AI, integrating with the LLM API to generate responses.

* **SmartGPTConsumerAdmin**: A specialized consumer for admin interactions, providing additional functionality and control for administrative users.

Integration and Flexibility
---------------------------

django-polly is designed to integrate seamlessly with your Django project:

* It extends Django's admin interface, allowing easy management of Parrots and SmartConversations.
* It provides URL routing for both HTTP and WebSocket connections.
* The application is built to be extensible, allowing you to add custom LLM backends or extend existing functionality.

Like Django Channels, django-polly operates on the principle of "turtles all the way down". Each component, from the high-level SmartConversation down to the low-level LLMInvoker, is designed to be a self-contained, reusable unit that can be composed into larger applications.

Getting Started
---------------

To start using django-polly, you'll need to:

1. Install the package and its dependencies
2. Configure your Django settings to include django-polly
3. Set up ASGI for WebSocket support
4. Create Parrot instances through the admin interface
5. Implement views or consumers that use SmartConversations

For detailed setup instructions, see the Quick Start guide below.

With django-polly, you can easily add AI-powered conversations, chatbots, content generation, and more to your Django projects. Whether you're building a customer service portal, an educational platform, or a creative writing tool, django-polly provides the foundation for integrating powerful AI capabilities into your web applications.