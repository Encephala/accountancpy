from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import JournalForm
from .models import Journal


# Create your views here.
def overview(request):
    return render(request, "journals/overview.html")


class JournalDetails(generic.DetailView):
    model = Journal
    template_name = "journals/details.html"


class JournalList(generic.ListView):
    model = Journal
    template_name = "journals/content/list.html"
    ordering = "id"


class JournalCreate(generic.CreateView):
    model = Journal
    template_name = "journals/create_update.html"
    success_url = reverse_lazy("journals:overview")
    form_class = JournalForm


class JournalUpdate(generic.UpdateView):
    model = Journal
    template_name = "journals/create_update.html"
    success_url = reverse_lazy("journals:overview")
    form_class = JournalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class JournalDelete(generic.DeleteView):
    model = Journal
    template_name = "journals/delete.html"
    success_url = reverse_lazy("journals:overview")

    def post(self, request, *args, **kwargs):
        try:
            super().post(request, *args, **kwargs)
        except ProtectedError as err:
            messages.error(request, "Journal has entries and thus cannot be deleted.")

            context = self.get_context_data(**kwargs)
            context["protected_objects"] = err.protected_objects
            return self.render_to_response(context)

        return redirect(self.get_success_url())
