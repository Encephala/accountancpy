from django.urls import path

from . import views

app_name = "ledgers"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("list/", views.LedgersList.as_view(), name="ledger_list"),
    path("<ledger_id>/", views.LedgerView.as_view(), name="view"),
]
