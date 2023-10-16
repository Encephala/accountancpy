from django.urls import path

from . import views

app_name = "journals"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("list/", views.JournalList.as_view(), name = "list"),
    path("create/", views.JournalCreate.as_view(), name = "create"),
    path("<pk>/", views.JournalDetails.as_view(), name = "details"),
    path("<pk>/update/", views.JournalUpdate.as_view(), name = "update"),
    path("<pk>/delete/", views.JournalDelete.as_view(), name = "delete"),
]
