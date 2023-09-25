from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("list/", views.EntryList.as_view(), name = "entry_list"),
    path("<entry_id>/", views.EntryList.as_view(), name = "details"),
    path("by-entry/<entry_id>/", views.EntryRowByEntry.as_view(), name = "entry_rows"),
    path("by-ledger/<ledger_id>/", views.EntryRowByLedger.as_view(), name = "ledger_rows"),
]
