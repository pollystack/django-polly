from django.shortcuts import render
from .models import Parrot


def parrot_list(request):
    parrots = Parrot.objects.all()
    return render(request, 'django_polly/parrot_list.html', {'parrots': parrots})
