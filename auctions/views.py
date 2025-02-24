from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auc_listing, Auc_comment, Bid, Category


def index(request):
    listings = Auc_listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
    })

def listings(request,id):
    info = Auc_listing.objects.get(pk=id)
    owner = True if request.user.username == info.owner.username else False
    comments = Auc_comment.objects.filter(listing=info)
    watchlist = request.user in info.watchlist.all()
    return render(request, "auctions/listings.html", {
        "info": info,
        "owner": owner,
        "comments": comments,
        "watchlist": watchlist
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

@login_required
def addListing(request):
    if request.method == "POST":
        starting_bid = Bid(bid_value=int(request.POST['starting_bid']), user_bid=request.user)
        starting_bid.save()
        new_listing = Auc_listing(
            title = request.POST['title'],
            description = request.POST['description'],
            current_bid = starting_bid,
            category = Category.objects.get(label=request.POST['category']),
            owner = request.user,
            url = request.POST['image_url']
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, "auctions/new.html", {
            "categories": Category.objects.all()
        })


@login_required
def create_comment(request, id):
    new_comment = Auc_comment(
        content = request.POST["comment"],
        listing = Auc_listing.objects.get(pk=id),
        user = request.user
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listings", args=(id, )))

@login_required
def close_auction(request, id):
    info = Auc_listing.objects.get(pk=id)
    info.active = False
    info.save()
    return render(request, "auctions/listings.html", {
        "info": info,
        "watchlist":  request.user in info.watchlist.all(),
        "comments": Auc_comment.objects.filter(listing=info),
        "owner": request.user.username == info.owner.username,
        "update": True,
        "message": "Auction closed"
    })



@login_required
def place_bid(request, id):
    add_bid = request.POST['bid']
    info = Auc_listing.objects.get(pk=id)
    comments = Auc_comment.objects.filter(listing=info)
    watchlist = request.user in info.watchlist.all()
    owner = True if request.user.username == info.owner.username else False
    if int(add_bid) > info.current_bid.bid_value:
        new_bid = Bid(user_bid=request.user, bid_value=int(add_bid))
        new_bid.save()
        info.current_bid = new_bid
        info.save()
        return render(request, "auctions/listings.html", {
            "info": info,
            "comments": comments,
            "watchlist": watchlist,
            "owner": owner,
            "message": "Bid accepted",
            "update": True,
        })
    else:
        return render(request, "auctions/listings.html", {
            "info": info,
            "comments": comments,
            "watchlist": watchlist,
            "owner": owner,
            "message": "Bid refused",
            "update": False,
        })

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

@login_required
def show_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all()
    })

@login_required
def add_watchlist(request, id):
    listing = Auc_listing.objects.get(pk=id)
    listing.watchlist.add(request.user)
    info = Auc_listing.objects.get(pk=id)
    return render(request, "auctions/listings.html", {
        "info": info,
        "watchlist":  request.user in info.watchlist.all(),
        "comments": Auc_comment.objects.filter(listing=info),
        "owner": request.user.username == info.owner.username,
        "update": True,
        "message": "Added to watchlist"
    })

@login_required
def remove_watchlist(request, id):
    listing = Auc_listing.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all()
    })

def categories(request):
    cat = request.POST['category']
    category = Category.objects.all()
    listings = Auc_listing.objects.filter(active=True, category=Category.objects.get(label=cat))
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": category,
        "message": f"Results for {cat}"
     })

