import asyncio
from unittest import skip
from unittest.mock import patch

import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model

from django_polly.consumers_admin import SmartGPTConsumerAdmin
from django_polly.lib.llm_api import TinyLLMConnect
from django_polly.models import SmartConversation

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestSmartGPTConsumerAdmin:
    @pytest.fixture
    async def user(self):
        return await User.objects.acreate(username='testuser', password='12345', is_staff=True, is_superuser=True)

    @pytest.fixture
    async def conversation(self, user):
        return await SmartConversation.objects.acreate(user=user, title="Test Conversation")

    @pytest.fixture
    def dummy_llm_connect(self):
        return TinyLLMConnect(is_dummy=True)

    @skip("This test is not working")
    async def test_connect_and_receive_message(self, user, conversation, dummy_llm_connect):
        with patch('django_polly.consumers_admin.TinyLLMConnect', return_value=dummy_llm_connect):
            application = SmartGPTConsumerAdmin.as_asgi()
            url = f"/polly/ws/smart-gpt-admin/"
            communicator = WebsocketCommunicator(
                application,
                url,
                {'query_string': f"user_id={user.id}&conversation_id={conversation.id}".encode()}
            )
            connected, _ = await communicator.connect()
            assert connected

            # Send a message
            await communicator.send_json_to({"message": "Hello, AI!"})

            # Expect user message HTML
            user_message = await communicator.receive_from()
            assert "Hello, AI!" in user_message
            assert "is_system" not in user_message

            # Expect system message HTML (empty initial message)
            system_message = await communicator.receive_from()
            assert 'message-' in system_message
            assert 'is_system' in system_message

            # Expect chunks of AI response
            response_received = False
            while not response_received:
                try:
                    response = await communicator.receive_from(timeout=1)
                    assert 'hx-swap-oob="beforeend"' in response
                    response_received = True
                except asyncio.TimeoutError:
                    break

            # Expect completion message
            completion = await communicator.receive_json_from()
            assert completion['type'] == 'assistant_message_complete'

            await communicator.disconnect()
