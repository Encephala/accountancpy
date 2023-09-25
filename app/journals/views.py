from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import *

# Create your views here.
def overview(request):
    return render(request, "journals/overview.html")


class JournalDetails(generic.DetailView):
    model = Journal
    template_name = "journals/details.html"

    def get_object(self):
        return get_object_or_404(self.model, id = self.kwargs["journal_id"])

class JournalList(generic.ListView):
    model = Journal
    template_name = "journals/content/list.html"
