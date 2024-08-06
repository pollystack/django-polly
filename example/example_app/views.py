# Create your views here.
from django.shortcuts import render
from django_polly.models import Parrot


def home(request):
    parrots = Parrot.objects.all()
    return render(request, 'example_app/home.html', {'parrots': parrots})