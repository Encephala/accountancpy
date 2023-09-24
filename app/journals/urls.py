from django.urls import path

from . import views

app_name = "journals"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("list/", views.JournalList.as_view(), name = "list"),
    path("<journal_id>/", views.JournalDetails.as_view(), name = "details"),
]
