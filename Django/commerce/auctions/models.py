from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    price = models.FloatField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=50, blank=True) 
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"UserID: {self.user.id}-ListingID: {self.id}"

class ActiveListing(Listing):
    pass

class PurchasedListing(Listing):
   pass 

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "listing"))
    
    def __str__(self):
        return f"UserID: {self.user.id}-ListingID: {self.listing.id}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.FloatField()
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "listing"))
    
    def __str__(self):
        return f"UserID: {self.user.id}-ListingID: {self.listing.id}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"UserID: {self.user.id}-ListingID: {self.listing.id}"