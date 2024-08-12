import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_polly.models import SmartConversation

User = get_user_model()

@pytest.mark.django_db
class TestSmartGPTChatView:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='12345', is_staff=True, is_superuser=True)

    @pytest.fixture
    def conversation(self, user):
        return SmartConversation.objects.create(user=user, title="Test Chat")

    def test_chat_view_with_valid_conversation(self, client, user, conversation):
        client.force_login(user)
        response = client.get(reverse('django_polly:smart_gpt_chat', args=[conversation.id]))
        assert response.status_code == 200
        assert 'conversation/single_chat.html' in [t.name for t in response.templates]

    def test_chat_view_with_invalid_conversation(self, client, user):
        client.force_login(user)
        response = client.get(reverse('django_polly:smart_gpt_chat', args=[999]))
        assert response.status_code == 404

    def test_chat_view_with_unauthorized_user(self, client, conversation):
        unauthorized_user = User.objects.create_user(username='unauthorized', password='12345')
        client.force_login(unauthorized_user)
        response = client.get(reverse('django_polly:smart_gpt_chat', args=[conversation.id]))
        assert response.status_code == 403
