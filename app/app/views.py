from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def redirect_home(request):
    return redirect("landing")

def http_404(request):
    return HttpResponse("<center><h1>Page not found.</h1><a href='/' style='font-size: 24'>Back to home</a></center>")
