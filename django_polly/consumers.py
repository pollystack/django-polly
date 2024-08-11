import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .lib.llm_api import TinyLLMConnect
from .models import SmartConversation, Message, ConversationParty

logger = logging.getLogger(__name__)


class SmartGPTConsumer(AsyncWebsocketConsumer):
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
        self.conversation = None

    @sync_to_async
    def init_chat_context(self, user_id, conversation_id=None):
        self.system_prompt = (
            self.system_prompt + ", You are now in a chat session with the user."
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

        # Send acknowledgment of user message
        await self.send(
            text_data=json.dumps({"type": "user_message", "message": message_text})
        )

        # Save user message to the conversation
        user_message = await sync_to_async(Message.objects.create)(
            conversation=self.conversation,
            content=message_text,
            party=ConversationParty.USER,
        )

        if not self.llm_connect or not self.llm_connect.llm_chat:
            error_message = "LLM not initialized properly. Please try again later."
            await self.send(
                text_data=json.dumps({"type": "error", "message": error_message})
            )
            return

        try:
            response_chunks = []
            async with asyncio.timeout(360):  # 360 seconds timeout, 6 minutes
                async for chunk in self.llm_connect.llm_chat.async_send_message_stream(
                    message_text
                ):
                    await self.send(
                        text_data=json.dumps(
                            {"type": "assistant_message_chunk", "message": chunk}
                        )
                    )
                    response_chunks.append(chunk)

            full_response = "".join(response_chunks)

            # Save assistant message to the conversation
            assistant_message = await sync_to_async(Message.objects.create)(
                conversation=self.conversation,
                content=full_response,
                party=ConversationParty.ASSISTANT,
            )

            # Send a message to indicate the full response is complete
            await self.send(
                text_data=json.dumps(
                    {"type": "assistant_message_complete", "message": full_response}
                )
            )

        except asyncio.TimeoutError:
            logger.error("Operation timed out")
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": "Operation timed out. Please try again.",
                    }
                )
            )
        except Exception as e:
            logger.exception(f"Error during message streaming: {e}")
            error_message = (
                "An error occurred while processing your request. Please try again."
            )
            await self.send(
                text_data=json.dumps({"type": "error", "message": error_message})
            )
