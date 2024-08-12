import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django_polly.admin import ParrotAdmin, SmartConversationAdmin
from django_polly.models import Parrot, SmartConversation

User = get_user_model()


class MockRequest:
    def __init__(self):
        self.session = {}
        self._messages = FallbackStorage(self)


def get_request_with_session():
    request = RequestFactory().get('/')
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()

    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    return request


@pytest.mark.django_db
class TestParrotAdmin:
    @pytest.fixture
    def admin(self):
        return ParrotAdmin(Parrot, AdminSite())

    @pytest.fixture
    def parrots(self):
        return [Parrot.objects.create(name=f"Parrot{i}", color="Red", age=i) for i in range(3)]

    def test_make_colorful_action(self, admin, parrots):
        request = get_request_with_session()
        queryset = Parrot.objects.all()

        admin.make_colorful(request, queryset)

        for parrot in Parrot.objects.all():
            assert parrot.color == 'Rainbow'


@pytest.mark.django_db
class TestSmartConversationAdmin:
    @pytest.fixture
    def admin(self):
        return SmartConversationAdmin(SmartConversation, AdminSite())

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='12345')

    @pytest.fixture
    def conversation(self, user):
        return SmartConversation.objects.create(user=user, title="Test Chat")

    def test_chat_button(self, admin, conversation):
        chat_button_html = admin.chat_button(conversation)
        assert 'class="button"' in chat_button_html
        assert 'target="_blank"' in chat_button_html
        assert f'/polly/smart-gpt-chat/{conversation.id}/' in chat_button_html
