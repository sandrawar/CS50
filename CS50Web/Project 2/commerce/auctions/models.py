from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    title = models.TextField(max_length=64)
    description = models.TextField()
    bid = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.URLField(blank=True)
    class Category(models.TextChoices):
        FASHION = "Fashion"
        TOYS = "Toys"
        ELECTRONICS = "Electronics"
        HOME = "Home"
        BOOKS = "Books"
    #category = models.TextField(choices=Category.choices)

class Bid(models.Model):
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
class User(AbstractUser):
    listings = models.ManyToManyField(Listing, blank=True, related_name="owner")