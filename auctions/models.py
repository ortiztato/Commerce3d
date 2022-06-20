

# from distutils.command.upload import upload
# from email.mime import image
# from tkinter import CASCADE
# from turtle import ondrag, title
# from unicodedata import bidirectional
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Category (models.Model):
    categorytype = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.categorytype}"

class Bid (models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.price}"

class Comment (models.Model):
    commenttext = models.TextField(max_length=300)
    commentuser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="rel_commentuser")

    def __str__(self):
        return f"{self.commentuser}: {self.commenttext}"

class Auction (models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(blank=True,upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="rel_category")
    bid = models.ManyToManyField(Bid, blank=True, related_name="rel_bid")
    initialbid = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    pricebidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="rel_pricebidder")
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="rel_owner")
    active = models.BooleanField(default=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name="rel_comments")
    watchuser = models.ManyToManyField(User, blank=True, related_name="rel_watchuser")

    def __str__(self):
        return f"{self.title}: {self.description}"