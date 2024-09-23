from django.urls import path

from . import views

app_name = "bookmark"

urlpatterns = [
    path("", views.list_items, name="list_items"),
]
