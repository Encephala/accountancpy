from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("hx-list/", views.EntryList.as_view(), name = "hx-list"),

    path("create/", views.EntryCreate.as_view(), name = "create"),
    # path("create-row/", views.EntryRowCreate.as_view(), name = "create_row"),

    path("<pk>/", views.EntryDetails.as_view(), name = "details"),
    path("<pk>/update/", views.EntryUpdate.as_view(), name = "update"),
    path("<pk>/delete/", views.EntryDelete.as_view(), name = "delete"),

    path("hx-rows-by-entry/<pk>/", views.EntryRowByEntry.as_view(), name = "hx-entry_rows"),
    path("hx-rows-by-ledger/<pk>/", views.EntryRowByLedger.as_view(), name = "hx-ledger_rows"),
    path("hx-rows-by-account/<pk>/", views.EntryRowByAccount.as_view(), name = "hx-account_rows"),
    path("hx-rows-by-journal/<pk>/", views.EntryByJournal.as_view(), name = "hx-journal_rows"),
]
