from django.shortcuts import render

#from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse



from .models import Auction, Category, Bid, Comment, User

# Create your views here.
def index(request):
    return render(request, "auctions/index.html",{
        "auctions": Auction.objects.all(),
        "categories": Category.objects.all(),
        "bids": Bid.objects.all()
    })

def create(request):
    return render(request, "auctions/createauction.html",{
        "categories": Category.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def fromcreate(request):
    if request.method == "POST":
        title = request.POST["title"]
        bodyauction = request.POST["bodyauction"]
        image = request.FILES["image"]
        categorytype1 = request.POST["category"]
        category1 = Category.objects.get(categorytype=categorytype1)
        initialbid=request.POST["bid"]
        bid1 = Bid.objects.create(price=initialbid)
        owner = request.user
        f = Auction(title=title, description=bodyauction, image=image, category=category1, initialbid=initialbid, price=initialbid, owner=owner) #revisar de unificarlo como el anterior
        f.save()
        f.bid.add(bid1)
    return HttpResponseRedirect(reverse("index"))

def auctiondetails(request, auction):
    g = Auction.objects.get(title=auction)
    comments = g.comments.all()
    if request.user in g.watchuser.all():
        watch=True
    else:
        watch=False
    return render(request, "auctions/auction.html",{
        "auction": g,
        "comments":comments,
        "watch":watch

    })

def placebid(request, auction):
    g = Auction.objects.get(title=auction)
    pricebidder=request.user
    if request.method == "POST":
        newbid=request.POST["bid"]
        bid1 = Bid.objects.create(price=newbid)
        g.price=newbid
        g.pricebidder=pricebidder
        g.save()
        g.bid.add(bid1)
    return HttpResponseRedirect(reverse("auctiondetails", args=[auction]))

def closeauction(request, auction):
    g = Auction.objects.get(title=auction)
    g.active=False
    g.save()
    return HttpResponseRedirect(reverse("auctiondetails", args=[auction]))

def comment(request, auction):
    g = Auction.objects.get(title=auction)
    commentuser=request.user
    if request.method == "POST":
        commenttext=request.POST["comment"]
        comment1 = Comment.objects.create(commenttext=commenttext, commentuser=commentuser)
        g.comments.add(comment1)
    return HttpResponseRedirect(reverse("auctiondetails", args=[auction]))

def changewatch(request, auction):
    g = Auction.objects.get(title=auction)
    if request.user in g.watchuser.all():
        g.watchuser.remove(request.user)
    else: 
        g.watchuser.add(request.user)
    return HttpResponseRedirect(reverse("auctiondetails", args=[auction]))

def watchlist(request):
    g = request.user
    watchauctions = g.rel_watchuser.all()
    return render(request, "auctions/watchlist.html",{
        "user": g,
        "watchauctions": watchauctions

    })

def categories(request):
    return render(request, "auctions/categoriesindex.html",{
        "categories": Category.objects.all()

    })

def category(request, categorytype):
    categorytype = categorytype
    category = Category.objects.get(categorytype=categorytype)
    auctionscat = category.rel_category.all()
    return render(request, "auctions/category.html",{
        "auctionscat": auctionscat,
        "auctions": Auction.objects.all(),
        "category": categorytype

    })