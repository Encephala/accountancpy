from django.urls import path

from . import views

app_name = "journals"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("list/", views.JournalList.as_view(), name = "list"),
    path("create/", views.JournalCreate.as_view(), name = "create"),
    path("update/<pk>/", views.JournalUpdate.as_view(), name = "update"),
    path("delete/<pk>/", views.JournalDelete.as_view(), name = "delete"),
    path("<pk>/", views.JournalDetails.as_view(), name = "details"),
]
