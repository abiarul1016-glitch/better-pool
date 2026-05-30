from django.urls import path

from . import views

app_name = "carpool"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("signup", views.signup, name="signup"),
]
