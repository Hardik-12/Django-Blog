from django.urls import path
from . import views


urlpatterns = [
    path("", views.Index, name="index"),
    path("posts", views.AllPosts, name="all_posts"),
    path("posts/<slug:slug>", views.PostDetail, name="post_detail"),
    path("posts/<slug:slug>/comments", views.AllComments, name="all_comments"),
    path("read_later", views.ReadLater, name="read-later"),
    path("signup", views.SignUpPage, name="signup"),
    path("login", views.LoginPage, name="login"),
    path("logout", views.LogoutPage, name="logout"),
]


