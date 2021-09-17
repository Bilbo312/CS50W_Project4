
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.get_profile, name="profile"),
    path("follow/<str:username>/<str:action>", views.follow, name="follow"),
    path("followers/<str:username>", views.followers, name="followers"),
    path("following", views.following_posts, name="following_posts"),
    path("like/<int:post_id>/<str:status>", views.like, name = "like"),
    path("edit", views.edit, name="edit"),
]
