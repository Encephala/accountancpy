from django.shortcuts import render, redirect
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
        context["entry_list"] = self.get_queryset().annotate(num_rows = Count("entryrow"))
        return context


class EntryCreate(generic.CreateView):
    model = Entry
    template_name = "entries/create_update.html"
    form_class = EntryForm

    def get_success_url(self):
        return reverse_lazy("entries:overview")

    def get_object(self, queryset = None):
        return queryset

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        entryform = EntryForm(request.POST)

        if entryform.is_valid():
            entry = entryform.save(commit = False)

            entryrow_formset = EntryRowFormSet(request.POST)

            if entryrow_formset.is_valid():
                # If everything is valid, we can save stuff
                entry.save()

                entryrows_instances = entryrow_formset.save(commit = False)

                for instance in entryrows_instances:
                    instance.entry = entry
                    instance.save()

                return redirect(self.get_success_url())

            return self.form_invalid(entryform, entryrow_formset)

        return self.form_invalid(entryform, entryrow_formset)

    def form_invalid(self, entryform, entryrow_formset):
        context = self.get_context_data(form = entryform, entryrow_formset = entryrow_formset)
        return self.render_to_response(context)

    def get_context_data(self, entryrow_formset = None, **kwargs):
        context = super().get_context_data(**kwargs)

        if entryrow_formset:
            context["entryrow_formset"] = entryrow_formset
        else:
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
