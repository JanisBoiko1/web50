from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listingitem/<int:listing_id>", views.listingitem, name="listingitem"),
    path("listingitem/<int:listing_id>/bid", views.bid, name="bid"),
    path("listingitem/<int:listing_id>/add", views.add, name="add"),
    path("listingitem/<int:listing_id>/remove", views.remove, name="remove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listingitem/<int:listing_id>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categoryItems/<int:category_id>", views.categoryItems, name="category"),
    path("close/<int:listing_id>", views.close, name="closeBid"),
]
