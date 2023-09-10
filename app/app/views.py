from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.
def my_404(request):
    # TODO: Dit via template doen
    return HttpResponseNotFound("<center><h1>Page not found.</h1><a href='/' style='font-size: 24'>Back to home</a></center>")
