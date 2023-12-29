import logging
logger = logging.getLogger("django")

from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from django.db.models import ProtectedError
from django.contrib import messages

from .models import Ledger
from .forms import LedgerForm

# Create your views here.
def overview(request):
    return render(request, "ledgers/overview.html")


class LedgerDetails(generic.DetailView):
    model = Ledger
    template_name = "ledgers/details.html"

    # This should probably be a method like entryrow_sum rather than this hacked context_data
    # Which leads me to wonder, can you call an object method in a templated file? would be banger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ledger_sum"] = context["object"].sum()
        return context


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
            messages.error(request, "Ledger is protected and cannot be deleted.")

            context = self.get_context_data(**kwargs)
            context["protected_objects"] = set([row.entry for row in err.protected_objects])
            return self.render_to_response(context)

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ledger_sum"] = context["object"].sum()
        return context


# HTMX endpoints
class LedgersList(generic.ListView):
    model = Ledger
    template_name = "ledgers/content/ledger_list.html"
    ordering = "id"

    def get_queryset(self):
        """Return first 50 Ledgers."""
        return Ledger.objects.all()[:50]


