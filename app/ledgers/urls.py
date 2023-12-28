from django.urls import path

from . import views

app_name = "ledgers"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("hx-list/", views.LedgersList.as_view(), name="hx-list"),
    path("create/", views.LedgerCreate.as_view(), name="create"),
    path("<pk>/", views.LedgerDetails.as_view(), name="details"),
    path("<pk>/update/", views.LedgerUpdate.as_view(), name="update"),
    path("<pk>/delete/", views.LedgerDelete.as_view(), name="delete"),
]
