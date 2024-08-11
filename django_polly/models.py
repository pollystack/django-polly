from django.db import models

from django.contrib.auth import get_user_model

from django_polly.lib.llm_api import LLMModelType

User = get_user_model()


class CommonFieldsModel(models.Model):
    external_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Parrot(CommonFieldsModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    model = models.CharField(choices=LLMModelType.choices(), default=LLMModelType.QWEN2_INSTRUCT, max_length=255)

    def __str__(self):
        return self.name


class Trick(CommonFieldsModel):
    parrot = models.ForeignKey(Parrot, on_delete=models.CASCADE, related_name='tricks')
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ])
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} (performed by {self.parrot.name})"


class SmartConversation(CommonFieldsModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ConversationParty(models.TextChoices):
    USER = 'USER', 'User'
    ASSISTANT = 'ASSISTANT', 'Assistant'


class Message(CommonFieldsModel):
    conversation = models.ForeignKey(SmartConversation, on_delete=models.CASCADE)
    content = models.TextField()
    party = models.CharField(max_length=10, choices=ConversationParty.choices)
