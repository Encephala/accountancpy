from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("list/", views.EntryList.as_view(), name = "list"),
    path("rows-by-entry/<pk>/", views.EntryRowByEntry.as_view(), name = "entry_rows"),
    path("rows-by-ledger/<pk>/", views.EntryRowByLedger.as_view(), name = "ledger_rows"),
    path("rows-by-account/<pk>/", views.EntryRowByAccount.as_view(), name = "account_rows"),
    path("entry-by-journal/<pk>/", views.EntryByJournal.as_view(), name = "journal_rows"),
    path("<pk>/", views.EntryDetails.as_view(), name = "details"),
]
