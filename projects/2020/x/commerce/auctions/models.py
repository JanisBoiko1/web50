#from _typeshed import SupportsReadline
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField
from django.db.models.fields.files import ImageField
from django.utils import timezone
import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=100)
    
    def __str__ (self):
        return f"{self.category}."

class Listing(models.Model):
    item_title = models.CharField(max_length=100)
    description = models.CharField(max_length = 2200, blank=True)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(blank=True)
    category = models.ForeignKey(Category, default=0, on_delete=models.CASCADE, related_name="itemCategory")
    final_bid = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(blank=True)
    timestanp = models.DateTimeField(auto_now_add=True, auto_now=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User,  default=[0], blank=True, null=True, related_name="watchedListing")
    buyer = models.ForeignKey(User, default=0, blank=True, null=True, on_delete=models.CASCADE, related_name="bidder")
    
    def __str__ (self):
        return f"{self.item_title}: {self.owner}. Startgin bid: {self.starting_bid}. Current bid: {self.final_bid}. {self.active}."
    
class Bid(models.Model):
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__ (self):
        return f"{self.bidder} bade {self.bid} on {self.item_id}."

class Comments(models.Model):
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 2200, blank=True)
    
    def __str__ (self):
        return f"{self.commenter} on item {self.item_id}: {self.comment}."

