from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("list/", views.EntryList.as_view(), name = "list"),

    path("create/", views.EntryCreate.as_view(), name = "create"),
    path("rows-create/<int:index>/", views.EntryRowCreate.as_view(), name = "create_row"),

    path("<pk>/", views.EntryDetails.as_view(), name = "details"),
    path("<pk>/update", views.EntryUpdate.as_view(), name = "update"),
    path("<pk>/delete", views.EntryDelete.as_view(), name = "delete"),

    path("rows-by-entry/<pk>/", views.EntryRowByEntry.as_view(), name = "entry_rows"),
    path("rows-by-ledger/<pk>/", views.EntryRowByLedger.as_view(), name = "ledger_rows"),
    path("rows-by-account/<pk>/", views.EntryRowByAccount.as_view(), name = "account_rows"),
    path("by-journal/<pk>/", views.EntryByJournal.as_view(), name = "journal_rows"),
]
