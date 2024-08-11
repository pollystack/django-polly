import pytest
from django.conf import settings
from channels.routing import ProtocolTypeRouter
from django_polly.routing import polly_asgi_routes


def test_installed_apps():
    assert 'django_polly' in settings.INSTALLED_APPS
    assert 'rest_framework' in settings.INSTALLED_APPS
    assert 'django_json_widget' in settings.INSTALLED_APPS


def test_asgi_application():
    assert hasattr(settings, 'ASGI_APPLICATION')
    assert settings.ASGI_APPLICATION == 'your_project.asgi.application'


def test_channel_layers():
    assert hasattr(settings, 'CHANNEL_LAYERS')
    assert 'default' in settings.CHANNEL_LAYERS
    assert settings.CHANNEL_LAYERS['default']['BACKEND'] == 'channels.layers.InMemoryChannelLayer'


def test_ai_models_path():
    assert hasattr(settings, 'AI_MODELS_PATH')
    assert settings.AI_MODELS_PATH is not None


@pytest.mark.django_db
def test_asgi_routing():
    from your_project.asgi import application
    assert isinstance(application, ProtocolTypeRouter)
    assert 'http' in application.application_mapping
    assert 'websocket' in application.application_mapping


def test_polly_asgi_routes():
    assert 'websocket' in polly_asgi_routes
    assert polly_asgi_routes['websocket'] is not None
