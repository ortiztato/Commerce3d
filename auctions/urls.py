
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createauction", views.create, name="createauction"),
    path("fromcreate", views.fromcreate, name="fromcreate"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("auctiondetails/<str:auction>", views.auctiondetails, name="auctiondetails"),
    path("placebid/<str:auction>", views.placebid, name="placebid"),
    path("closeauction/<str:auction>", views.closeauction, name="closeauction"),
    path("comment/<str:auction>", views.comment, name="comment"),
    path("changewatch/<str:auction>", views.changewatch, name="changewatch"),
    path("category/<str:categorytype>", views.category, name="category"),


]
