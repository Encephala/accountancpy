from django.shortcuts import render, get_list_or_404
from django.views import generic
from django.urls import reverse_lazy

from .models import Entry, EntryRow
from .forms import EntryForm, EntryRowForm

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


class EntryCreate(generic.CreateView):
    model = Entry
    template_name = "entries/create_update.html"
    form_class = EntryForm

    # Show details of created Entry
    def get_success_url(self, **kwargs):
        return reverse("entries:details", pk = self.object.pk)


class EntryUpdate(generic.UpdateView):
    pass


class EntryDelete(generic.DeleteView):
    pass


# HTMX endpoints
class EntryRowCreate(generic.CreateView):
    model = EntryRow
    template_name = "entries/content/entryrow_create_update.html"
    form_class = EntryRowForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["index"] = self.kwargs["index"]
        return context


class EntryRowByLedger(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entryrow_list.html"
    context_object_name = "entry_row_list"
    ordering = "id"

    def get_queryset(self):
        return EntryRow.objects.filter(ledger = self.kwargs["pk"])


class EntryRowByEntry(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entryrow_list.html"
    context_object_name = "entry_row_list"
    ordering = "id"

    def get_queryset(self):
        return EntryRow.objects.filter(entry = self.kwargs["pk"])


class EntryRowByAccount(generic.ListView):
    model = EntryRow
    template_name = "entries/content/entryrow_list.html"
    context_object_name = "entry_row_list"
    ordering = "id"

    def get_queryset(self):
        return EntryRow.objects.filter(account = self.kwargs["pk"])


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
