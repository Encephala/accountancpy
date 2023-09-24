from django.db import models
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import generic

from .models import Entry, EntryRow

from django.db.models import Count

# Create your views here.
def overview(request):
    return render(request, "entries/overview.html")


class EntryDetails(generic.DetailView):
    model = Entry
    template_name = "entries/details.html"

    def get_object(self, queryset = None):
        return get_object_or_404(self.model, id = self.kwargs["entry_id"])

class EntryList(generic.ListView):
    model = Entry
    template_name = "entries/content/entry_list.html"

    # Annotate entries with num_rows
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = self.get_queryset().annotate(num_rows = Count("entryrow"))
        context["entry_list"] = entries
        return context



class EntryRowByLedger(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"

    def get_queryset(self):
        return get_list_or_404(self.model, ledger = self.kwargs["ledger_id"])


class EntryRowByEntry(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"

    def get_queryset(self):
        return get_list_or_404(self.model, entry = self.kwargs["entry_id"])


class EntryRowByAccount(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"

    def get_queryset(self):
        return get_list_or_404(self.model, account = self.kwargs["account_id"])


class EntryByJournal(generic.ListView):
    model = Entry
    template_name = "entries/content/entry_list.html"

    # Annotate entries with num_rows
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = self.get_queryset().annotate(num_rows = Count("entryrow"))
        context["entry_list"] = entries
        return context
