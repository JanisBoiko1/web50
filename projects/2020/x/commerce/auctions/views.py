from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import User, Listing, Bid, Comments, Category
from .forms import ListingForm, BidForm, CommentsForm

def index(request):
    return render(request, "auctions/index.html", {
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
def newlisting(request):
    
    #get form
    form = ListingForm(request.POST or None)
        
    if request.method == "POST":
        #get data from form
        if form.is_valid():
            instance = form.save(commit = False)
            
            # owner = User.objects.get(id=int(request.POST["owner"]))
            # instance.owner = owner
            
            #check if all the obrigatory data was provided
            item_title = form.cleaned_data.get("item_title")
            if not item_title:
                messages.error(request, "missing item title")
                
            description= form.cleaned_data.get("description")
            if not description:
                messages.error(request, "missing item description")
                
            starting_bid = form.cleaned_data.get("starting_bid")
            
            if not starting_bid:
                messages.error(request, "missing starting bid")
            
            #set final bid value to $0,00
            final_bid = form.cleaned_data.get("final_bid")
            if (final_bid != 0.00):
                final_bid=0.00
            instance.final_bid = final_bid
            instance.active = True
            # watchers =[]
            # instance.watchers.set(watchers)
            instance.owner = request.user
            instance.buyer = User.objects.get(id=3)
                
            instance.save()
            return render(request, "auctions/save.html", {})
    
        
    return render(request, "auctions/newlisting.html", {
        "form": form, 
        "users": User.objects.all()
        })
    
def listingitem(request, listing_id):
    #all info about the listing
    listing = Listing.objects.get(id=listing_id)
    
    #bidding form
    form = BidForm(request.POST or None)
    
    #commenting form
    form2 = CommentsForm(request.POST or None)
    
    #for user who is the owner
    if request.user == listing.owner:
        listing.is_owner = True
        
    else:
        listing.is_owner = False
        
    #for user watcher
    if request.user in listing.watchers.all():
        listing.is_watcher = True
        
    else:
        listing.is_watcher = False
    
    #for user buyer
    if request.user == listing.buyer:
        listing.is_buyer = True
        
    else:
        listing.is_buyer = False
      
    #get comments  
    
    remarks=Comments.objects.filter(item_id=listing_id)
    
    if remarks:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "form":form,
        "form2":form2,
        "remarks": remarks,
        })

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form":form,
        "form2":form2,
        "remarks": [],
        })

@login_required
def add(request, listing_id):
    #get user id
    user = request.user
    
    #get Listing
    listing = Listing.objects.get(id=listing_id)
    #add user to watchers
    listing.watchers.add(user)
    
    return HttpResponseRedirect(reverse("listingitem", args=(listing_id,)))

@login_required    
def remove(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    
    #get user id
    user = request.user
    
    #remove user from watchers
    listing.watchers.remove(user)
    
    return HttpResponseRedirect(reverse("listingitem", args=(listing_id,)))

@login_required    
def bid(request, listing_id):
    form2 = CommentsForm(request.POST or None)
    
    form = BidForm(request.POST or None)
   
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        instance = form.save(commit = False)
        if instance.bid < listing.starting_bid:
            messages.error(request, "Bid must be higher.")
            
        if instance.bid <= listing.final_bid:
            messages.error(request, "Bid must be higher.")
        if ((instance.bid > listing.final_bid) and (instance.bid >= listing.starting_bid)):    
            instance.bidder = user
            instance.item_owner = listing.owner
            instance.item_id = Listing.objects.get(id=listing_id)
            instance.save()
            Listing.objects.filter(id=listing_id).update(final_bid=instance.bid)
            
            messages.success(request, "Your bid was accepted.")
            listing.refresh_from_db()
                    
    return render(request, "auctions/listing.html", {
     "listing": listing,
     "form": form,
     "form2": form2})
    
@login_required 
def watchlist(request):
    user = request.user
    listings = user.watchedListing.all()
    if listings:
        return render(request, "auctions/watchlist.html", {
            "listings":listings
        })

    return render(request, "auctions/watchlist.html", {"message": "You have no items in your Watchlist."
        })

def categories(request):
    
    categories = Category.objects.all()
    if categories:
        return render(request, "auctions/categories.html", {"categories": categories
        })
    else:
        return render(request, "auctions/categories.html", {"message": "There are no categories defined yet."
        })
    
def categoryItems(request, category_id):
    categories = Category.objects.get(id=category_id)
    
    #  listings = user.watchedListing.all()
    listings = categories.itemCategory.all()
    if listings:
        return render(request, "auctions/category.html", {
            "name": categories.category.capitalize(),
            "listings":listings
        })
    else:
        return render(request, "auctions/category.html", {
            "name": categories.category.capitalize(),
            "message":"No listings in this category yet."
        })
    
@login_required    
def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form2 = CommentsForm(request.POST or None)
    user = request.user
    
    if form2.is_valid():
        instance = form2.save(commit = False)
        instance.commenter = user
        instance.item_id = Listing.objects.get(id=listing_id)
        instance.save()
            
    return HttpResponseRedirect(reverse("listingitem", args=(listing_id,)))    
       

@login_required    
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.buyer = Bid.objects.filter(item_id = listing).last().bidder
    listing.active = False
    listing.save()
        
    return HttpResponseRedirect(reverse("listingitem", args=(listing_id,)))