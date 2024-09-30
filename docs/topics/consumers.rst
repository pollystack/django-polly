Consumers
=========

In Django Polly, consumers are responsible for handling WebSocket connections and facilitating real-time communication between users and AI models (Parrots).

SmartGPTConsumer
----------------

The `SmartGPTConsumer` is the primary consumer class in Django Polly. It handles WebSocket connections for chat functionality.

Key Features:
^^^^^^^^^^^^^

1. Asynchronous message handling
2. Integration with LLM API for AI responses
3. Management of SmartConversations

Usage Example:
^^^^^^^^^^^^^^

.. code-block:: python

    from django_polly.consumers import SmartGPTConsumer

    class MyChatConsumer(SmartGPTConsumer):
        async def receive(self, text_data):
            # Custom logic here
            await super().receive(text_data)

SmartGPTConsumerAdmin
---------------------

The `SmartGPTConsumerAdmin` extends `SmartGPTConsumer` with additional functionality for administrative users.

Key Features:
^^^^^^^^^^^^^

1. Enhanced control and monitoring capabilities
2. Access to advanced LLM parameters
3. Ability to manage multiple conversations

Iframe Access for ChatUI
------------------------

The ChatUI can now be accessed via an iframe using an API key. This feature allows secure embedding of the ChatUI in other applications.

Key Features:
^^^^^^^^^^^^^

1. Secure access using API keys
2. Embeddable iframe for ChatUI
3. Validation of API key and conversation ID

Usage Example:
^^^^^^^^^^^^^^

To access the ChatUI via an iframe, use the following URL format:

.. code-block:: html

    <iframe src="https://yourdomain.com/iframe-chat/?conversation_id=SomeID&api_key=SomeKey" width="600" height="400"></iframe>

For more details on implementing and customizing consumers, see the API reference.
