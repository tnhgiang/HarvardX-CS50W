from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from .models import User, ActiveListing, PurchasedListing, Watchlist, Bid, Comment
from .forms import ListingForm

def index(request):
    active_listings = ActiveListing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": active_listings
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

@login_required()
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image_url = form.cleaned_data['image_url']
            category = form.cleaned_data['category']

            listing = ActiveListing(
                user=user, title=title,
                description=description,
                price=price, image_url=image_url,
                category=category
            )
            listing.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create_listing.html", {
            "form": ListingForm()
        })

@login_required
def manipulate_listing(request, id):
    try:
        listing = ActiveListing.objects.get(id=id)
        user = request.user

        bids = Bid.objects.filter(listing=listing)
        comments = Comment.objects.filter(listing=listing)

        if len(bids) == 0:
            bid_info = {
                'count': 0, 'max_bid': 0,
                'acceptive_price': listing.price
            }
        else:
            bid_info = {
                'count': bids.count(), 
                'max_bid': bids.aggregate(Max('amount'))['amount__max'],
                'acceptive_price': bids.aggregate(Max('amount'))['amount__max']
            }

        try:
            current_bid = Bid.objects.get(user=user, listing=listing)
        except Bid.DoesNotExist:
            current_bid = None
            bid_amount = 0
        else:
            bid_amount = current_bid.amount

        bid_info.update({'current_bid': bid_amount})
            
    except ActiveListing.DoesNotExist:
        return HttpResponse("Bad request!")
    
    else:
        if request.method == 'POST':

            if 'button' in request.POST:
                button_value = request.POST['button']

                if button_value == 'close':
                    if len(bids) != 0:
                        winner = Bid.objects.get(listing=listing, amount=bid_info['max_bid']).user
                        purchased_listing = PurchasedListing(
                            user=winner, title=listing.title,
                            price=bid_info['max_bid'],
                            description=listing.description,
                            image_url=listing.image_url,
                            category=listing.category
                        )

                        purchased_listing.save()
                    listing.delete()

                    return HttpResponseRedirect(reverse("index"))

                elif button_value == 'add':
                    watchlist_item = Watchlist(user=user, listing=listing)
                    watchlist_item.save()

                elif button_value == 'remove':
                    watchlist_item = Watchlist.objects.get(user=user, listing=listing)
                    watchlist_item.delete()
            
                elif button_value == 'place-bid':
                    bid_amount = float(request.POST['bid'])
                    # TODO: The min_value is unconsistant between HTML and Django
                    # TODO: HTML >= min_value, while Django > min_value
                    if bid_amount > bid_info['acceptive_price']:
                        if current_bid:
                            current_bid.amount = bid_amount
                            current_bid.save()
                        else:
                            bid = Bid(user=user, listing=listing, amount=bid_amount)
                            bid.save()
                    else:
                        # TODO: Output an error message to notify the user
                        pass

                elif button_value == 'add-comment':
                    content = request.POST['comment']
                    if content:
                        comment = Comment(user=user, listing=listing, content=content)
                        comment.save()

            return HttpResponseRedirect(
                reverse("manipulate_listing", kwargs={'id': listing.id})
            )

        else:
            if request.user == listing.user:
                user_info = 'owner'
            else:
                try:
                    watchlist_item = Watchlist.objects.get(
                        user=user, listing=listing
                    )
                except Watchlist.DoesNotExist:
                    user_info = 'Not in watchlist'
                else:
                    user_info = 'In watchlist'

            return render(request, "auctions/listing.html", {
                "listing": listing,
                'bid_info': bid_info,
                "user_info": user_info,
                "comments": comments
            })

@login_required
def check_watchlist(request):
    user = request.user

    try:
        listings = Watchlist.objects.filter(user=user)
        listings = [record.listing for record in listings]

    except Watchlist.DoesNotExist:
        listings = Watchlist.objects.none()
    
    return render(request, "auctions/index.html", {
        "listings": listings
    })

@login_required
def check_purchase_list(request):
    user = request.user

    try:
        listings = PurchasedListing.objects.filter(user=user)

    except Watchlist.DoesNotExist:
        listings = Watchlist.objects.none()
    
    return render(request, "auctions/purchase_list.html", {
        "listings": listings
    })

def categories(request):
    listings = ActiveListing.objects.all()

    categories = []
    for listing in listings:
        category = listing.category
        if category and category not in categories:
            categories.append(category)
    
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
@login_required
def show_category(request, category):
    listings = ActiveListing.objects.filter(category=category)

    return render(request, "auctions/index.html", {
       "listings": listings 
    })
    
