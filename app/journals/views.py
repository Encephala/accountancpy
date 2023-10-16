from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy

from .models import *
from .forms import JournalForm

# Create your views here.
def overview(request):
    return render(request, "journals/overview.html")


class JournalDetails(generic.DetailView):
    model = Journal
    template_name = "journals/details.html"


class JournalCreate(generic.CreateView):
    model = Journal
    template_name = "journals/create_update.html"
    success_url = reverse_lazy("journals:overview")
    form_class = JournalForm


class JournalUpdate(generic.UpdateView):
    pass


class JournalDelete(generic.DeleteView):
    pass


class JournalList(generic.ListView):
    model = Journal
    template_name = "journals/content/list.html"
    ordering = "id"
