"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""  # noqa: D413
from django.contrib import admin
from django.urls import include, path

from . import views

handler404 = views.my_404

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("empty/", views.empty, name="empty"),  # HTMX endpoint to delete elements
    path("", views.landing, name="landing"),
    path("ledgers/", include("ledgers.urls")),
    path("entries/", include("entries.urls")),
    path("accounts/", include("accounts.urls")),
    path("journals/", include("journals.urls")),
]
