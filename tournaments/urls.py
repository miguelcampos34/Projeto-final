from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_tournament, name="create_tournament"),
    path("tournament/<int:tournament_id>", views.tournament_detail, name="tournament_detail"),
    path("tournament/<int:tournament_id>/add_player", views.add_player, name="add_player"),
]