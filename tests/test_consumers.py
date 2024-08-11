import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django_polly.consumers import SmartGPTConsumer
from django_polly.models import SmartConversation

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestSmartGPTConsumer:
    @pytest.fixture
    async def user(self):
        return await User.objects.create_user(username='testuser', password='12345')

    @pytest.fixture
    async def conversation(self, user):
        return await SmartConversation.objects.create(user=user, title="Test Conversation")

    async def test_connect(self, user, conversation):
        communicator = WebsocketCommunicator(
            SmartGPTConsumer.as_asgi(),
            f"/polly/ws/smart-gpt/{conversation.id}/?user_id={user.id}"
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_receive_message(self, user, conversation):
        communicator = WebsocketCommunicator(
            SmartGPTConsumer.as_asgi(),
            f"/polly/ws/smart-gpt/{conversation.id}/?user_id={user.id}"
        )
        await communicator.connect()

        await communicator.send_json_to({"message": "Hello, AI!"})
        response = await communicator.receive_json_from()

        assert response['type'] == 'user_message'
        assert response['message'] == 'Hello, AI!'

        # Wait for AI response
        ai_response = await communicator.receive_json_from()
        assert ai_response['type'] == 'assistant_message_chunk'

        await communicator.disconnect()
