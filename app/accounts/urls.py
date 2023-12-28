from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("hx-list/", views.AccountList.as_view(), name = "hx-list"),
    path("<pk>/", views.AccountDetails.as_view(), name = "details"),
]
