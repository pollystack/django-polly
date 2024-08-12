Models
======

Django Polly provides several models to represent AI entities and conversations in your application.

Parrot
------

The `Parrot` model represents an instance of a Language Learning Model (LLM).

Fields:
^^^^^^^

- `name`: CharField, the name of the Parrot
- `color`: CharField, a descriptive color for the Parrot
- `age`: IntegerField, the age of the Parrot
- `model`: CharField, the specific LLM model type
- `external_id`: CharField, an optional external identifier

Methods:
^^^^^^^^

- `__str__`: Returns the name of the Parrot

SmartConversation
-----------------

The `SmartConversation` model represents an ongoing dialogue between a user and a Parrot.

Fields:
^^^^^^^

- `user`: ForeignKey to User model
- `title`: CharField, the title of the conversation
- `external_id`: CharField, an optional external identifier

Methods:
^^^^^^^^

- `__str__`: Returns a string representation of the conversation

Message
-------

The `Message` model represents individual messages within a SmartConversation.

Fields:
^^^^^^^

- `conversation`: ForeignKey to SmartConversation
- `content`: TextField, the content of the message
- `party`: CharField, indicates whether the message is from the USER or ASSISTANT
- `external_id`: CharField, an optional external identifier

Methods:
^^^^^^^^

- `__str__`: Returns a truncated version of the message content

Usage Example:
--------------

.. code-block:: python

    from django_polly.models import Parrot, SmartConversation, Message

    # Create a new Parrot
    parrot = Parrot.objects.create(name="Polly", color="Green", age=3, model="QWEN2_INSTRUCT")

    # Create a new SmartConversation
    conversation = SmartConversation.objects.create(user=request.user, title="My First Chat")

    # Add messages to the conversation
    Message.objects.create(conversation=conversation, content="Hello, Polly!", party="USER")
    Message.objects.create(conversation=conversation, content="Hello! How can I assist you today?", party="ASSISTANT")

For more details on model fields and methods, refer to the API reference.