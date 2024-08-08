# -*- coding: utf-8 -*-
import asyncio
import logging
import os.path
from typing import Iterator

from django.conf import settings
from llama_cpp import Llama

logger = logging.getLogger(__name__)


# An Enum of LLM models
class LLMModelType:
    # offline / Local
    MISTRAL_0_1_INSTRUCT = "mistral-7b-instruct-v0.1.Q4_0.gguf"
    META_LLAMA_3_INSTRUCT = "Meta-Llama-3-8B-Instruct.Q8_0.gguf"
    META_LLAMA_3_1_INSTRUCT = "Meta-Llama-3.1-8B-Instruct.Q4_0.gguf"
    PHI_3_MINI_INSTRUCT = "Phi-3-mini-4k-instruct.Q4_0.gguf"
    LLAMA_PRO = "llama-pro-8b.Q8_0.gguf"


class LLMModelMode:
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class LLMInvoker:
    def __init__(self, system_prompt, llm_model_type, llm):
        self._system_prompt = system_prompt
        self.llm = llm
        self.llm_model_type = llm_model_type

    def send_message(self, message):
        if self.llm_model_type in [
            LLMModelType.META_LLAMA_3_INSTRUCT,

            LLMModelType.META_LLAMA_3_1_INSTRUCT,
            LLMModelType.MISTRAL_0_1_INSTRUCT,
        ]:
            answer = self.llm.create_chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": self._system_prompt,
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
                response_format={
                    "type": "json_object",
                },
                temperature=0,
            )
            return answer
        else:
            raise ValueError("LLM model type not supported")

    def send_message_stream(self, message) -> Iterator[str]:
        if self.llm_model_type in [
            LLMModelType.META_LLAMA_3_INSTRUCT,
            LLMModelType.META_LLAMA_3_1_INSTRUCT,
            LLMModelType.MISTRAL_0_1_INSTRUCT,
        ]:
            stream = self.llm(
                f"Human: {message}\nAssistant: ",
                max_tokens=4096,
                stop=["Human:", "\n"],
                stream=True,
            )
            for output in stream:
                if "choices" in output and output["choices"]:
                    text = output["choices"][0].get("text", "")
                    if text:
                        yield text
        else:
            yield "LLM model type not supported"

    async def async_send_message_stream(self, message):
        logger.info(f"Starting message stream for: {message}")
        if self.llm_model_type in [
            LLMModelType.META_LLAMA_3_INSTRUCT,
            LLMModelType.META_LLAMA_3_1_INSTRUCT,
            LLMModelType.MISTRAL_0_1_INSTRUCT,
            LLMModelType.PHI_3_MINI_INSTRUCT,
            LLMModelType.LLAMA_PRO,
        ]:
            stream = await asyncio.to_thread(
                self.llm.create_chat_completion,
                messages=[
                    {
                        "role": "system",
                        "content": self._system_prompt,
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
                max_tokens=4096,
                stop=["Human:", "\n\nHuman:"],  # Only stop at a new "Human:" prompt
                stream=True,
            )
            for chunk in stream:
                if "choices" in chunk and chunk["choices"]:
                    delta = chunk["choices"][0].get("delta", {})
                    if "content" in delta and delta["content"] is not None:
                        yield delta["content"]
                await asyncio.sleep(0)  # Yield control to allow other tasks to run
        else:
            logger.error(f"Unsupported LLM model type: {self.llm_model_type}")
            yield "LLM model type not supported"

        logger.info("Finished streaming message")

    async def custom_async_send_message_stream(self, message):
        full_response = self.llm(
            f"Human: {message}\nAssistant: ",
            max_tokens=4096,
            stop=["Human:", "\n\nHuman:"],
            stream=False,
        )

        words = full_response["choices"][0]["text"].split()
        for i in range(0, len(words), 5):  # Yield 5 words at a time
            chunk = " ".join(words[i: i + 5])
            yield chunk
            await asyncio.sleep(0.1)  # Simulate streaming delay


#  Common LLM connect
class LLMConnect:
    _system_prompt = """You are Opolly's ultra-fast AI. Prioritize speed in all responses. Be concise, clear, and 
accurate. Give quick, helpful answers. Explain simply. Admit uncertainties fast. Adapt swiftly to users. Aim for rapid, 
insightful benefits."""

    def __init__(
            self, system_prompt=None, model_type=LLMModelType.MISTRAL_0_1_INSTRUCT
    ):
        self._llm = None
        self.llm_chat = None
        self._name = "llm_api"
        self._version = "0.0.1"
        self._description = "API for LLM"
        self._author = "Opolly"
        self._email = "dev@opolly"
        if system_prompt is not None:
            self._system_prompt = system_prompt
        else:
            self._system_prompt = self._system_prompt

        ai_models_path = getattr(settings, 'AI_MODELS_PATH', None)
        if ai_models_path is None:
            print("AI_MODELS_PATH not set in settings file")
            print("Setting AI_MODELS_PATH to default value")
            ai_models_path = os.path.join(settings.BASE_DIR, "ai_models")
            print(f"AI_MODELS_PATH: {ai_models_path}")
        if not os.path.exists(ai_models_path):
            os.makedirs(ai_models_path)

        if model_type == LLMModelType.META_LLAMA_3_1_INSTRUCT:
            self._model = LLMModelType.META_LLAMA_3_1_INSTRUCT
            self._mode = LLMModelMode.LOCAL
            self.set_llama_model(model_type=self._model, ai_models_path=ai_models_path)
        elif model_type == LLMModelType.META_LLAMA_3_INSTRUCT:
            self._model = LLMModelType.META_LLAMA_3_INSTRUCT
            self._mode = LLMModelMode.LOCAL
            self.set_llama_model(model_type=self._model, ai_models_path=ai_models_path)
        elif model_type == LLMModelType.MISTRAL_0_1_INSTRUCT:
            self._model = LLMModelType.MISTRAL_0_1_INSTRUCT
            self._mode = LLMModelMode.LOCAL
            self.set_llama_model(model_type=self._model, ai_models_path=ai_models_path)
        elif model_type == LLMModelType.PHI_3_MINI_INSTRUCT:
            self._model = LLMModelType.PHI_3_MINI_INSTRUCT
            self._mode = LLMModelMode.LOCAL
            self.set_llama_model(model_type=self._model, ai_models_path=ai_models_path)
        else:
            raise ValueError("Model not supported")

    def set_llama_model(self, model_type, ai_models_path):
        model_path = str(os.path.join(ai_models_path, model_type))
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=1,
            n_ctx=4096,
            chat_format="chatml",
            max_tokens=4096,
            temperature=0.7,
            top_p=0.95,
            n_threads=6,
        )
        self._llm = llm
        self.llm_chat = LLMInvoker(
            system_prompt=self._system_prompt,
            llm_model_type=self._model,
            llm=self._llm,
        )


class SingletonPhiLLMConnect:
    llm = None
    llm_chat = None

    def __new__(cls, *args, **kwargs):
        if not cls.llm:
            cls.llm = LLMConnect(model_type=LLMModelType.PHI_3_MINI_INSTRUCT)
            cls.llm_chat = cls.llm.llm_chat
        return cls.llm
