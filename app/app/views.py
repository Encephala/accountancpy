from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def landing(request):
    return render(request, "landing.html")

def empty(request):
    return HttpResponse("")

def my_404(request, exception = None):
    return render(request, "404.html", { "exception": exception })

def favicon(request):
    return redirect("static/media/icon_ledger.svg", permanent = True)
