from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.overview, name="overview"),
]
