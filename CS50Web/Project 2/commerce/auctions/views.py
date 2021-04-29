from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from operator import attrgetter

from .models import User, Listing, Bid, Watchlist


def index(request):
    return render(request, "auctions/active.html", {
        "listings": Listing.objects.all()
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

@login_required
def create(request):
    if request.method == "POST":
        try:
            title = request.POST["title"]
            description = request.POST["description"]
            bid = request.POST["bid"]
            category = request.POST["category"]
        except IntegrityError:
            return render(request, "auctions/create.html", {
                "message": "Not all data provided."
            })
        photo = ''
        try:
            photo = request.POST["photo"]   
        except:
            pass
        listing = Listing(title=title, description=description, minimalPrice=bid, photo=photo, category=category, owner=request.user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    
def listing(request, listing):
    product = Listing.objects.get(id=listing)
    bids = product.bids.order_by('-price').all()[:2]
    if len(bids) == 0:
        currentprice = product.minimalPrice
    elif len(bids) == 1:
        currentprice = product.minimalPrice + 1
    else:
        currentprice = bids[1].price + 1

    currentprice = product.minimalPrice
    return render(request, "auctions/listing.html", {
        "listing": product,
        "currentprice": currentprice
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        product = int(request.POST["product"])
        watchlist = Watchlist(user=request.user, listing=Listing.objects.get(id=product))
        watchlist.save()
        userWatchlist = []
        for listing in request.user.watchlist.order_by('id').all():
            userWatchlist.append(Listing.objects.get(id=listing.listing.id))
    return render(request, "auctions/watchlist.html", {
        "listings": userWatchlist
    })