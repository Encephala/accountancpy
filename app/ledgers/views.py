from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseBadRequest
from django.urls import reverse

from django.db.models import Sum

from .models import Ledger

# Create your views here.
def overview(request):
    return render(request, "ledgers/overview.html")


class LedgerDetails(generic.DetailView):
    model = Ledger
    template_name = "ledgers/details.html"

    def get_object(self, queryset = None):
        return get_object_or_404(Ledger, pk = self.kwargs["ledger_id"])

    # This should probably be a method like entryrow_sum rather than this hacked context_data
    # Which leads me to wonder, can you call an object method in a templated file? would be banger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ledger_sum"] = context["object"].entryrow_set.aggregate(sum = Sum("value"))["sum"]
        return context


# My half-assed attempt at creating my own CreateView
# Shows the page on which you create a new thingy
def new(request):
    return render(request, "ledgers/new.html")


# Takes a POST request and creates thingy and redirects to overview view
def create(request):
    try:
        id = request.POST.get("id")
        name = request.POST.get("name")
        type = request.POST.get("type")
        notes = request.POST.get("notes")

        Ledger(id, name, type, notes).save()
    except TypeError as err:
        return HttpResponseBadRequest(err)


    # Redirect to Ledger ListView
    return redirect(reverse("ledgers:overview"))


# HTMX endpoints
class LedgersList(generic.ListView):
    model = Ledger
    template_name = "ledgers/content/ledger_list.html"
    ordering = "id"

    def get_queryset(self):
        """Return first 50 Ledgers."""
        return Ledger.objects.all()[:50]


