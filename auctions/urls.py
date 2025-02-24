from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("new", views.addListing, name="new"),
    path("closer_auction/<int:id>", views.close_auction, name="close_auction"),
    path("create_comment/<int:id>", views.create_comment, name="create_comment"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("show_watchlist", views.show_watchlist, name="show_watchlist"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("categories", views.categories, name="categories"),
]  
