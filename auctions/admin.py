from django.contrib import admin
from .models import Auction, Category, Bid, Comment, User

# Register your models here.
admin.site.register(Auction)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)