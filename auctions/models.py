from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid_value = models.IntegerField()
    def __str__(self):
        return str(self.bid_value)

class Category(models.Model):
    label = models.CharField(max_length=50)
    def __str__(self):
        return self.label

class Auc_listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    current_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    url = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True,related_name="watchlist")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="owner")

class Auc_comment(models.Model):
    content = models.TextField()
    listing = models.ForeignKey(Auc_listing, on_delete=models.CASCADE, related_name='listing')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

