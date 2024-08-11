import asyncio
import json
import uuid
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from lib.llm_api import LLMConnect, LLMModelType, TinyLLMConnect

logger = logging.getLogger(__name__)


class SmartGPTConsumerAdmin(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.messages = []
        self.system_prompt = """
You are a very helpful AI assistant. You have to be very fast, speed is of paramount in your conversations. 
You are very knowledgeable and can provide information on a wide range of topics. Make sure your answers are detailed 
and informative. You are very polite and respectful. You are very patient and can handle any type of user.
"""
        self.document_message = None
        self.llm_connect = None

    @sync_to_async
    def init_chat_context(self):
        self.system_prompt = (
            self.system_prompt + ", You are now in a chat session with the user."
        )
        try:
            self.llm_connect = TinyLLMConnect()
            if not self.llm_connect.llm_chat:
                raise ValueError("LLM chat not initialized properly")
        except Exception as e:
            logger.error(f"Failed to initialize LLMConnect: {e}")
            self.llm_connect = None

    async def connect(self, *args, **kwargs):
        await self.init_chat_context()
        await super().connect()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]

        user_message_html = render_to_string(
            "conversation/ws/chat_message.html",
            {
                "message_text": message_text,
                "is_system": False,
            },
        )
        await self.send(text_data=user_message_html)
        self.messages.append(
            {
                "role": "user",
                "content": message_text,
            }
        )
        message_id = f"message-{uuid.uuid4().hex}"
        system_message_html = render_to_string(
            "chat_demo/ws/chat_message.html",
            {"message_text": "", "is_system": True, "message_id": message_id},
        )
        await self.send(text_data=system_message_html)

        if not self.llm_connect or not self.llm_connect.llm_chat:
            error_message = "LLM not initialized properly. Please try again later."
            await self.send(
                text_data=f'<div id="{message_id}" hx-swap-oob="beforeend">{error_message}</div>'
            )
            return

        try:
            response_chunks = []
            async with asyncio.timeout(360):  # 360 seconds timeout, 6 minutes
                async for chunk in self.llm_connect.llm_chat.async_send_message_stream(
                    message_text
                ):
                    formatted_chunk = chunk.replace("\n", "<br>")
                    await self.send(
                        text_data=f'<div id="{message_id}" hx-swap-oob="beforeend">{formatted_chunk}</div>'
                    )
                    response_chunks.append(chunk)

            full_response = "".join(response_chunks)
            self.messages.append({"role": "assistant", "content": full_response})
        except asyncio.TimeoutError:
            logger.error("Operation timed out")
            await self.send(text_data="Operation timed out. Please try again.")
        except Exception as e:
            logger.exception(f"Error during message streaming: {e}")
            error_message = (
                "An error occurred while processing your request. Please try again."
            )
            await self.send(
                text_data=f'<div id="{message_id}" hx-swap-oob="beforeend">{error_message}</div>'
            )
