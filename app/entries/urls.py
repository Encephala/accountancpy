from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("view/<entry_id>/", views.EntryRowByEntry.as_view(), name = "view"),
    path("by-ledger/<ledger_id>/", views.EntryRowByLedger.as_view(), name = "ledger_rows"),
]
