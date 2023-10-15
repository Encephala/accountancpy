from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import *

# Create your views here.
def overview(request):
    return render(request, "accounts/overview.html")


class AccountDetails(generic.DetailView):
    model = Account
    template_name = "accounts/details.html"


class AccountList(generic.ListView):
    model = Account
    template_name = "accounts/content/accounts_list.html"
    ordering = "id"
