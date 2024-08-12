import pytest
from django.contrib.auth import get_user_model
from django_polly.models import Parrot, SmartConversation, Message, ConversationParty
from django_polly.lib.llm_api import LLMModelType

User = get_user_model()


@pytest.mark.django_db
class TestParrotModel:
    def test_parrot_creation(self):
        parrot = Parrot.objects.create(
            name="Polly",
            color="Green",
            age=3,
            model=LLMModelType.QWEN2_INSTRUCT.value
        )
        assert parrot.name == "Polly"
        assert parrot.color == "Green"
        assert parrot.age == 3
        assert parrot.model == LLMModelType.QWEN2_INSTRUCT.value

    def test_parrot_str_representation(self):
        parrot = Parrot.objects.create(name="Charlie", color="Blue", age=5)
        assert str(parrot) == "Charlie"


@pytest.mark.django_db
class TestSmartConversationModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='12345')

    def test_conversation_creation(self, user):
        conversation = SmartConversation.objects.create(
            user=user,
            title="Test Conversation"
        )
        assert conversation.user == user
        assert conversation.title == "Test Conversation"

    def test_conversation_str_representation(self, user):
        conversation = SmartConversation.objects.create(user=user, title="My Chat")
        assert str(conversation) == "Conversation 1 - My Chat"


@pytest.mark.django_db
class TestMessageModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='12345')

    @pytest.fixture
    def conversation(self, user):
        return SmartConversation.objects.create(user=user)

    def test_message_creation(self, conversation):
        message = Message.objects.create(
            conversation=conversation,
            content="Hello, AI!",
            party=ConversationParty.USER
        )
        assert message.conversation == conversation
        assert message.content == "Hello, AI!"
        assert message.party == ConversationParty.USER

    def test_message_str_representation(self, conversation):
        message = Message.objects.create(
            conversation=conversation,
            content="A very long message that should be truncated in the string representation",
            party=ConversationParty.ASSISTANT
        )
        assert str(message) == "ASSISTANT: A very long message that should be truncated in th..."
