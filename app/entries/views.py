from django.shortcuts import render, get_list_or_404
from django.views import generic

from .models import Entry, EntryRow

from django.db.models import Count

# Create your views here.
def overview(request):
    return render(request, "entries/overview.html")


class EntryDetails(generic.DetailView):
    model = Entry
    template_name = "entries/details.html"


class EntryList(generic.ListView):
    model = Entry
    template_name = "entries/content/entry_list.html"
    ordering = "id"

    # Annotate entries with num_rows
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry_list"] =  self.get_queryset().annotate(num_rows = Count("entryrow"))
        return context


class EntryRowByLedger(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"
    ordering = "id"


class EntryRowByEntry(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"
    ordering = "id"


class EntryRowByAccount(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entry_row_list.html"
    context_object_name = "entry_row_list"
    ordering = "id"


class EntryByJournal(generic.ListView):
    model = Entry
    template_name = "entries/content/entry_list.html"
    ordering = "id"

    # Annotate entries with num_rows
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry_list"] = self.get_queryset().annotate(num_rows = Count("entryrow"))
        return context

    def get_queryset(self):
        return Entry.objects.filter(journal = self.kwargs["pk"])
