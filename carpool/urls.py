from django.urls import path

from . import views

app_name = "carpool"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("signup", views.signup, name="signup"),
    path("login", views.login_user, name="login"),
    path("profile", views.profile_view, name="profile"),
    path("carpool-group/<int:group_id>", views.group_details, name="group_details"),
]
