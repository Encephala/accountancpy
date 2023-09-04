from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def landing(request):
    return HttpResponse("<h1>Welkom op de landing page, episch</h1>\n")
