from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    #listings = models.ManyToManyField(Listing, blank=True, related_name="owner")
    #watchlist = models.ManyToManyField(Listing, blank=True, related_name="observators")

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.TextField(max_length=64)
    description = models.TextField()
    minimalPrice = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.URLField(blank=True)
    class Category(models.TextChoices):
        FASHION = "Fashion"
        TOYS = "Toys"
        ELECTRONICS = "Electronics"
        HOME = "Home"
        BOOKS = "Books"
    category = models.TextField(choices=Category.choices)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="observators")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")


