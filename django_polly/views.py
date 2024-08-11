from django.db import models
from django.db.models import Avg
from django.views.generic import TemplateView
from django.template.response import TemplateResponse

from .models import Parrot, Trick


def chat(request):
    return TemplateResponse(request, "conversation/single_chat.html")


class DashboardView(TemplateView):
    template_name = "django_polly/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_parrots'] = Parrot.objects.count()
        context['previous_total_parrots'] = context['total_parrots'] - 5  # This is a placeholder calculation
        context['total_tricks'] = Trick.objects.count()
        context['avg_tricks_per_parrot'] = Parrot.objects.annotate(trick_count=models.Count('tricks')).aggregate(Avg('trick_count'))['trick_count__avg'] or 0
        context['recent_parrots'] = Parrot.objects.all().order_by('-id')[:5]
        return context
