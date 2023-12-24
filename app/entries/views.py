from django.shortcuts import render, get_list_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import Entry, EntryRow
from .forms import EntryForm, EntryRowFormSet

from django.db.models import Count

import logging
logger = logging.getLogger("django")

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
    success_url = reverse_lazy(f"entries:list")

    def post(self, request, *args, **kwargs):
        entry = EntryForm(request.POST)
        self.object = entry


        if entry.is_valid():
            entry = entry.save(commit = False)

            entryrows = EntryRowFormSet(request.POST)


            if entryrows.is_valid():
                entry.save()
                for row in entryrows:
                    logger.info(f"row: {row.visible_fields()}")
                    row.fields["entry"] = entry
                    row.save()

                return render(self.get_success_url())

            logger.info(f"entryrows invalid {entryrows.errors} {entryrows.non_form_errors()}")
            return self.form_invalid(self.object)

        logger.info(f"entry invalid {entry.non_field_errors()}")
        return self.form_invalid(self.object)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["entryrow_formset"] = EntryRowFormSet(queryset = EntryRow.objects.none())
        context["is_update"] = False

        return context

class EntryUpdate(generic.UpdateView):
    pass

class EntryDelete(generic.DeleteView):
    pass


# HTMX endpoints
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
