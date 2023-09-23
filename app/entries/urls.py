from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("<entry_id>/", views.EntryRowView.as_view(), name = "single_row"),
]
