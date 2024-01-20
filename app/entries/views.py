from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .models import Entry, EntryRow
from .forms import EntryForm, EntryRowFormSet, EntryRowUpdateFormSet

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

    def post(self, request, *args, **kwargs):
        self.object = None

        entry_form = EntryForm(request.POST)
        entryrow_formset = EntryRowFormSet(request.POST)

        if entry_form.is_valid() and entryrow_formset.is_valid():
            entry = entry_form.save()

            entryrow_instances = entryrow_formset.save(commit = False)

            for instance in entryrow_instances:
                instance.entry = entry
                instance.save()

            return redirect(self.get_success_url())

        return self.form_invalid(entry_form, entryrow_formset)

    def form_invalid(self, entry_form, entryrow_formset):
        context = self.get_context_data(form = entry_form, entryrow_formset = entryrow_formset)

        return self.render_to_response(context)

    def get_context_data(self, entryrow_formset = None, **kwargs):
        kwargs["is_update"] = False

        if entryrow_formset:
            kwargs["entryrow_formset"] = entryrow_formset
        else:
            kwargs["entryrow_formset"] = EntryRowFormSet(queryset = EntryRow.objects.none())

        return super().get_context_data(**kwargs)


class EntryUpdate(generic.UpdateView):
    model = Entry
    template_name = "entries/create_update.html"
    form_class = EntryForm

    def get_success_url(self):
        return reverse_lazy("entries:details", kwargs = { "pk": self.object.pk })

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        entry_form = EntryForm(request.POST, instance = self.object)
        entryrow_formset = EntryRowUpdateFormSet(request.POST, instance = self.object)

        if entry_form.is_valid() and entryrow_formset.is_valid():
            entry_form.save()
            entryrow_formset.save()

            return redirect(self.get_success_url())

        return self.form_invalid(entry_form, entryrow_formset)

    def form_invalid(self, entry_form, entryrow_formset):
        context = self.get_context_data(form = entry_form, entryrow_formset = entryrow_formset)

        return self.render_to_response(context)

    def get_context_data(self, entryrow_formset = None, **kwargs):
        kwargs["is_update"] = True

        if entryrow_formset:
            kwargs["entryrow_formset"] = entryrow_formset
        else:
            kwargs["entryrow_formset"] = EntryRowUpdateFormSet(instance = self.object)

        return super().get_context_data(**kwargs)

class EntryDelete(generic.DeleteView):
    model = Entry
    template_name = "entries/delete.html"
    success_url = reverse_lazy("entries:overview")


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
