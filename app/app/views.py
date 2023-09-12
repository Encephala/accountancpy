from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

# Create your views here.
def landing(request):
    return render(request, "landing.html")


def my_404(request):
    template = loader.get_template("404.html")

    return HttpResponseNotFound(template.render({}, request))
