from django.contrib import admin
from .models import Listing, ActiveListing, PurchasedListing, Watchlist, Bid, Comment

# Register your models here.
admin.site.register(Listing)
admin.site.register(ActiveListing)
admin.site.register(PurchasedListing)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comment)