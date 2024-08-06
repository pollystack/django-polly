from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Parrot


class DashboardView(TemplateView):
    template_name = "django_polly/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_parrots'] = Parrot.objects.count()
        context['parrots'] = Parrot.objects.all()[:5]  # Display the latest 5 parrots
        return context


def parrot_list(request):
    parrots = Parrot.objects.all()
    return render(request, 'django_polly/parrot_list.html', {'parrots': parrots})
