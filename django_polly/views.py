from django.db import models
from django.db.models import Avg
from django.views.generic import TemplateView
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponseForbidden, HttpResponseNotFound

from .models import Parrot, Trick, SmartConversation, APIKey


def smart_gpt_chat(request, conversation_id):
    try:
        conversation_id = int(conversation_id)
        conversation = SmartConversation.objects.get(id=conversation_id)
    except (ValueError, SmartConversation.DoesNotExist):
        return TemplateResponse(request, 'conversation/not_found.html', status=404)
    if conversation.user != request.user or not request.user.is_superuser or not request.user.is_staff:
        return TemplateResponse(request, 'conversation/access_denied.html', status=403)
    return render(request, 'conversation/single_chat.html', {'conversation_id': conversation_id,
                                                             'conversation_title': conversation.title})


def iframe_chat(request):
    api_key = request.GET.get('api_key')
    conversation_id = request.GET.get('conversation_id')

    if not api_key or not conversation_id:
        return HttpResponseForbidden("API key and conversation ID are required")

    try:
        api_key_obj = APIKey.objects.get(key=api_key)
    except APIKey.DoesNotExist:
        return HttpResponseForbidden("Invalid API key")

    try:
        conversation = SmartConversation.objects.get(id=conversation_id, user=api_key_obj.user)
    except SmartConversation.DoesNotExist:
        return HttpResponseNotFound("Conversation not found")

    return render(request, 'conversation/single_chat.html', {'conversation_id': conversation_id,
                                                             'conversation_title': conversation.title})


class DashboardView(TemplateView):
    template_name = "django_polly/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_parrots'] = Parrot.objects.count()
        context['previous_total_parrots'] = context['total_parrots'] - 5  # This is a placeholder calculation
        context['total_tricks'] = Trick.objects.count()
        context['avg_tricks_per_parrot'] = \
            Parrot.objects.annotate(trick_count=models.Count('tricks')).aggregate(Avg('trick_count'))[
                'trick_count__avg'] or 0
        context['recent_parrots'] = Parrot.objects.all().order_by('-id')[:5]
        return context
