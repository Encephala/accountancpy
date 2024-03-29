import logging
from typing import TYPE_CHECKING

from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from django.db.models import ProtectedError
from django.contrib import messages

from .models import Ledger
from .forms import LedgerForm

if TYPE_CHECKING:
    from entries.models import EntryRow

logger = logging.getLogger("django")


# Create your views here.
def overview(request):
    return render(request, "ledgers/overview.html")


class LedgerDetails(generic.DetailView):
    model = Ledger
    template_name = "ledgers/details.html"


class LedgerCreate(generic.CreateView):
    model = Ledger
    template_name = "ledgers/create_update.html"
    success_url = reverse_lazy("ledgers:overview")
    form_class = LedgerForm


class LedgerUpdate(generic.UpdateView):
    model = Ledger
    template_name = "ledgers/create_update.html"
    success_url = reverse_lazy("ledgers:overview")
    form_class = LedgerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class LedgerDelete(generic.DeleteView):
    model = Ledger
    template_name = "ledgers/delete.html"
    success_url = reverse_lazy("ledgers:overview")

    def post(self, request, *args, **kwargs):
        try:
            super().post(request, *args, **kwargs)
        except ProtectedError as err:
            messages.error(request, "Ledger has rows and thus cannot be deleted.")

            context = self.get_context_data(**kwargs)

            protected_objects: set[EntryRow] = err.protected_objects  # type: ignore reportGeneralTypeIssues
            context["protected_objects"] = {row.entry for row in protected_objects}
            return self.render_to_response(context)

        return redirect(self.get_success_url())


# HTMX endpoints
class LedgersList(generic.ListView):
    model = Ledger
    template_name = "ledgers/content/ledger_list.html"
    ordering = "id"

    def get_queryset(self):
        """Return first 50 Ledgers."""
        return Ledger.objects.all()[:50]
