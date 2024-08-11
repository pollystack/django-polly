import asyncio
import json
import logging
import uuid

from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from django_polly.lib.llm_api import TinyLLMConnect
from django_polly.models import SmartConversation, Message, ConversationParty

logger = logging.getLogger(__name__)

User = get_user_model()


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
        self.user = None

    @database_sync_to_async
    def init_chat_context(self, user_id, conversation_id=None):
        self.user = User.objects.get(id=user_id)
        if conversation_id:
            self.conversation = SmartConversation.objects.get(id=conversation_id)
        else:
            self.conversation = SmartConversation.objects.create(user_id=user_id)

        self.llm_connect = TinyLLMConnect()
        if not self.llm_connect.llm_chat:
            raise ValueError("LLM chat not initialized properly")

        # If it's a new conversation, add the greeting
        if self.conversation.messages.count() == 0:
            greeting = f"Hello {self.user.first_name}, what can I help you with today?"
            Message.objects.create(
                conversation=self.conversation,
                content=greeting,
                party=ConversationParty.ASSISTANT,
            )

    @database_sync_to_async
    def get_conversation_messages(self):
        return list(self.conversation.messages.order_by('created_at').values('content', 'party'))

    async def connect(self):
        await self.accept()

        query_string = self.scope.get("query_string", b"").decode()
        query_params = dict(param.split('=') for param in query_string.split('&') if param)

        user_id = query_params.get("user_id")
        conversation_id = query_params.get("conversation_id")
        if not user_id:
            await self.close(code=4000)
            return

        try:
            await self.init_chat_context(user_id, conversation_id)
        except Exception as e:
            logger.error(f"Failed to initialize chat context: {e}")
            await self.close(code=4002)
            return

        # Load and send existing messages
        messages = await self.get_conversation_messages()
        for message in messages:
            message_html = render_to_string(
                "conversation/ws/chat_message.html",
                {
                    "message_text": message['content'],
                    "is_system": message['party'] == ConversationParty.ASSISTANT,
                },
            )
            await self.send(text_data=message_html)

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
