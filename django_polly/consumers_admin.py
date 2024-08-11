import asyncio
import json
import logging
import uuid

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from django_polly.lib.llm_api import TinyLLMConnect
from django_polly.models import SmartConversation, Message, ConversationParty

logger = logging.getLogger(__name__)


class SmartGPTConsumerAdmin(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.messages = []
        self.system_prompt = """
You are a very helpful AI assistant for admin tasks. You have to be very fast, speed is of paramount in your conversations. 
You are very knowledgeable about admin operations and can provide detailed information. Make sure your answers are 
informative and tailored for admin users. You are professional and efficient in your responses.
"""
        self.document_message = None
        self.llm_connect = None
        self.conversation = None

    @sync_to_async
    def init_chat_context(self, user_id, conversation_id=None):
        self.system_prompt = (
            self.system_prompt + ", You are now in an admin chat session with the user."
        )
        try:
            self.llm_connect = TinyLLMConnect()
            if not self.llm_connect.llm_chat:
                raise ValueError("LLM chat not initialized properly")

            if conversation_id:
                self.conversation = SmartConversation.objects.get(id=conversation_id)
            else:
                self.conversation = SmartConversation.objects.create(user_id=user_id)

        except Exception as e:
            logger.error(f"Failed to initialize LLMConnect or SmartConversation: {e}")
            self.llm_connect = None
            self.conversation = None

    async def connect(self):
        await self.accept()
        user_id = self.scope["query_string"].decode().split("user_id=")[1]
        conversation_id = self.scope["url_route"]["kwargs"].get("conversation_id")
        await self.init_chat_context(user_id, conversation_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]

        # Render and send user message
        user_message_html = render_to_string(
            "conversation/ws/chat_message.html",
            {
                "message_text": message_text,
                "is_system": False,
            },
        )
        await self.send(text_data=user_message_html)

        # Save user message to the conversation
        await sync_to_async(Message.objects.create)(
            conversation=self.conversation,
            content=message_text,
            party=ConversationParty.USER,
        )

        if not self.llm_connect or not self.llm_connect.llm_chat:
            error_message = "Admin LLM not initialized properly. Please try again later."
            error_html = render_to_string(
                "conversation/ws/chat_message.html",
                {
                    "message_text": error_message,
                    "is_system": True,
                },
            )
            await self.send(text_data=error_html)
            return

        try:
            message_id = f"message-{uuid.uuid4().hex}"
            system_message_html = render_to_string(
                "conversation/ws/chat_message.html",
                {"message_text": "", "is_system": True, "message_id": message_id},
            )
            await self.send(text_data=system_message_html)

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

            # Save assistant message to the conversation
            await sync_to_async(Message.objects.create)(
                conversation=self.conversation,
                content=full_response,
                party=ConversationParty.ASSISTANT,
            )

        except asyncio.TimeoutError:
            logger.error("Admin operation timed out")
            timeout_message = "Admin operation timed out. Please try again."
            timeout_html = render_to_string(
                "conversation/ws/chat_message.html",
                {
                    "message_text": timeout_message,
                    "is_system": True,
                },
            )
            await self.send(text_data=timeout_html)
        except Exception as e:
            logger.exception(f"Error during admin message streaming: {e}")
            error_message = "An error occurred while processing your admin request. Please try again."
            error_html = render_to_string(
                "conversation/ws/chat_message.html",
                {
                    "message_text": error_message,
                    "is_system": True,
                },
            )
            await self.send(text_data=error_html)