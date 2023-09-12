from django.shortcuts import render
from django.views import generic

from .models import Ledger

# Create your views here.
# def overview(request):
#     return render(request, "ledgers/overview.html")


class Overview(generic.ListView):
    template_name = "ledgers/overview.html"

    def get_queryset(self):
        """Return first 50 Ledgers."""
        return Ledger.objects.all()[:50]
