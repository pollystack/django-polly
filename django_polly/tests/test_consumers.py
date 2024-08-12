import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django_polly.consumers import SmartGPTConsumer
from django_polly.models import SmartConversation
from django.urls import reverse

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestSmartGPTConsumer:
    @pytest.fixture
    async def user(self):
        return await User.objects.acreate(username='testuser', password='12345')

    @pytest.fixture
    async def conversation(self, user):
        return await SmartConversation.objects.acreate(user=user, title="Test Conversation")

    async def test_connect(self, user, conversation):
        application = SmartGPTConsumer.as_asgi()
        url = reverse('django_polly:smart_gpt', kwargs={'conversation_id': conversation.id})
        communicator = WebsocketCommunicator(
            application,
            f"{url}?user_id={user.id}",
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_receive_message(self, user, conversation):
        application = SmartGPTConsumer.as_asgi()
        url = reverse('django_polly:smart_gpt', kwargs={'conversation_id': conversation.id})
        communicator = WebsocketCommunicator(
            application,
            f"{url}?user_id={user.id}",
        )
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({"message": "Hello, AI!"})
        response = await communicator.receive_json_from()

        assert response['type'] == 'user_message'
        assert response['message'] == 'Hello, AI!'

        # Wait for AI response
        ai_response = await communicator.receive_json_from()
        assert ai_response['type'] == 'assistant_message_chunk'

        await communicator.disconnect()
