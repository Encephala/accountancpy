from django.urls import path

from . import views

app_name = "ledgers"

urlpatterns = [
    path("", views.overview, name="overview"),
]
