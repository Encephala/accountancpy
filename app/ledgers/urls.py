from django.urls import path

from . import views

app_name = "ledgers"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("list/", views.LedgersList.as_view(), name="list"),
    path("create/", views.LedgerCreate.as_view(), name="create"),
    path("update/<pk>/", views.LedgerUpdate.as_view(), name="update"),
    path("<pk>/", views.LedgerDetails.as_view(), name="details"),
]
