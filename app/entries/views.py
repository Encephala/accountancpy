from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import EntryRow

# Create your views here.
def overview(request):
    return render(request, "entries/_base.html")

class EntryRowView(generic.DetailView):
    model = EntryRow
    template_name = "entries/content/entry_row_view.html"
    context_object_name = "entry"

    def get_object(self, queryset = None):
        return get_object_or_404(EntryRow, pk = self.kwargs["entry_id"])
