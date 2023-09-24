from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

# Create your views here.
def landing(request):
    return render(request, "landing.html")


def my_404(request):
    return render(request, "404.html")

def favicon(request):
    return redirect("static/media/icon_ledger.svg", permanent = True)
