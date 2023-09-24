from django.shortcuts import render, get_list_or_404
from django.views import generic

from .models import EntryRow

# Create your views here.
def overview(request):
    return render(request, "entries/_base.html")


class EntryRowByLedger(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"

    def get_queryset(self):
        return get_list_or_404(EntryRow, ledger = self.kwargs["ledger_id"])


class EntryRowByEntry(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"

    def get_queryset(self):
        return get_list_or_404(EntryRow, entry = self.kwargs["entry_id"])
