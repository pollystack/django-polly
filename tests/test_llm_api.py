import pytest
from django_polly.lib.llm_api import LLMConnect, LLMModelType, LLMInvoker


class TestLLMConnect:
    def test_llm_connect_initialization(self):
        llm_connect = LLMConnect(model_type=LLMModelType.QWEN2_INSTRUCT)
        assert llm_connect.llm_chat is not None
        assert llm_connect._model == LLMModelType.QWEN2_INSTRUCT

    def test_llm_connect_with_custom_system_prompt(self):
        custom_prompt = "You are a helpful assistant."
        llm_connect = LLMConnect(system_prompt=custom_prompt)
        assert llm_connect._system_prompt == custom_prompt


class TestLLMInvoker:
    @pytest.fixture
    def invoker(self):
        llm_connect = LLMConnect(model_type=LLMModelType.QWEN2_INSTRUCT)
        return llm_connect.llm_chat

    def test_send_message(self, invoker):
        response = invoker.send_message("Hello, AI!")
        assert response is not None
        assert 'choices' in response

    @pytest.mark.asyncio
    async def test_async_send_message_stream(self, invoker):
        async for chunk in invoker.async_send_message_stream("Tell me a short story."):
            assert isinstance(chunk, str)
            assert len(chunk) > 0


class TestLLMModelType:
    def test_llm_model_types(self):
        model_types = LLMModelType.llm_model_types()
        assert 'QWEN2_INSTRUCT' in model_types
        assert 'MISTRAL_0_1_INSTRUCT' in model_types

    def test_model_supported(self):
        assert LLMModelType.model_supported('QWEN2_INSTRUCT')
        assert not LLMModelType.model_supported('NONEXISTENT_MODEL')
