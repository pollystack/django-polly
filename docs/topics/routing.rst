Routing
=======

Routing in Django Polly is handled through Django Channels, allowing you to manage both HTTP and WebSocket connections.

ASGI Application
----------------

Django Polly provides a pre-configured ASGI application that includes routing for both HTTP and WebSocket connections.

Usage:
^^^^^^

In your project's `asgi.py` file:

.. code-block:: python

    from django_polly.routing import polly_asgi_routes
    from channels.routing import ProtocolTypeRouter

    application = ProtocolTypeRouter(polly_asgi_routes)

Custom Routing
--------------

You can extend or customize the default routing by creating your own `ProtocolTypeRouter`:

.. code-block:: python

    from channels.routing import ProtocolTypeRouter, URLRouter
    from django.urls import path
    from .consumers import MyCustomConsumer

    application = ProtocolTypeRouter({
        "websocket": URLRouter([
            path("ws/chat/", MyCustomConsumer.as_asgi()),
            # Include Django Polly's default routing
            *polly_asgi_routes["websocket"],
        ]),
    })

URL Configuration
-----------------

Django Polly also provides URL patterns for HTTP endpoints. Include these in your project's `urls.py`:

.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        # ...
        path('polly/', include('django_polly.urls')),
    ]

For more advanced routing configurations, refer to the Django Channels documentation.