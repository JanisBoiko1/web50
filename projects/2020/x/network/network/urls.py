
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile" ),
    path("following", views.following_page, name="following"),
    
     # API Routes
    path("posts", views.compose, name="compose"),
    path("posts/<str:showGroup>/<int:user_id>", views.showPosts, name="showposts"),
    path("posts/<int:post_id>", views.individualPost, name="individualPost"),  
]
