import logging

from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from django.db.models import ProtectedError
from django.contrib import messages

from .models import Account
from .forms import AccountForm

logger = logging.getLogger("django")


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


class AccountCreate(generic.CreateView):
    model = Account
    template_name = "accounts/create_update.html"
    success_url = reverse_lazy("accounts:overview")
    form_class = AccountForm


class AccountUpdate(generic.UpdateView):
    model = Account
    template_name = "accounts/create_update.html"
    success_url = reverse_lazy("accounts:overview")
    form_class = AccountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class AccountDelete(generic.DeleteView):
    model = Account
    template_name = "accounts/delete.html"
    success_url = reverse_lazy("accounts:overview")

    def post(self, request, *args, **kwargs):
        try:
            super().post(request, *args, **kwargs)
        except ProtectedError as err:
            messages.error(request, "Account has rows and thus cannot be deleted.")

            context = self.get_context_data(**kwargs)
            context["protected_objects"] = set([row.entry for row in err.protected_objects])
            logger.info(f"{context['protected_objects']}")
            return self.render_to_response(context)

        return redirect(self.get_success_url())
