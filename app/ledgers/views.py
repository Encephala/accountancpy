from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Ledger

# Create your views here.
def overview(request):
    return render(request, "ledgers/overview.html")


class LedgerView(generic.DetailView):
    model = Ledger
    template_name = "ledgers/view.html"

    def get_object(self, queryset = None):
        return get_object_or_404(Ledger, pk = self.kwargs["ledger_id"])


# HTMX endpoints
class LedgersList(generic.ListView):
    template_name = "ledgers/content/list.html"

    def get_queryset(self):
        """Return first 50 Ledgers."""
        return Ledger.objects.all()[:50]
