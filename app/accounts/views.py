import logging

from typing import TYPE_CHECKING

from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

if TYPE_CHECKING:
    from entries.models import EntryRow

from .forms import AccountForm
from .models import Account

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
            protected_objects: set[EntryRow] = err.protected_objects  # type: ignore reportGeneralTypeIssues

            context["protected_objects"] = {row.entry for row in protected_objects}
            logger.info("%s", context["protected_objects"])
            return self.render_to_response(context)

        return redirect(self.get_success_url())
