from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newPage, name = "new_page"),
    path("search/", views.search, name = "search"),
    path("random", views.randomPage, name = "random"),
    path("<str:name>", views.entry , name="entry"),
    path("<str:name>/Edit", views.edit , name="edit")
]
