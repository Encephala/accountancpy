from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.overview, name = "overview"),
    path("hx-list/", views.AccountList.as_view(), name = "hx-list"),

    path("create/", views.AccountCreate.as_view(), name = "create"),

    path("<pk>/", views.AccountDetails.as_view(), name = "details"),
    path("<pk>/update/", views.AccountUpdate.as_view(), name = "update"),
    path("<pk>/delete/", views.AccountDelete.as_view(), name = "delete"),
]
