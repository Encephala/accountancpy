from django.http import HttpResponse
from django.shortcuts import redirect, render


# Create your views here.
def landing(request):
    return render(request, "landing.html")


def empty(request):  # noqa: ARG001
    return HttpResponse("")


def my_404(request, exception=None):
    return render(request, "404.html", {"exception": exception})


def favicon(request):  # noqa: ARG001
    return redirect("static/media/icon_ledger.svg", permanent=True)
