from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("list/", views.EntryList.as_view(), name = "entry_list"),
    path("rows-by-entry/<entry_id>/", views.EntryRowByEntry.as_view(), name = "entry_rows"),
    path("rows-by-ledger/<ledger_id>/", views.EntryRowByLedger.as_view(), name = "ledger_rows"),
    path("rows-by-account/<account_id>/", views.EntryRowByAccount.as_view(), name = "account_rows"),
    path("entry-by-journal/<journal_id>/", views.EntryByJournal.as_view(), name = "journal_rows"),
    path("<entry_id>/", views.EntryDetails.as_view(), name = "details"),
]
