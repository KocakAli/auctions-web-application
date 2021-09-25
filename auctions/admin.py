from django.contrib import admin
from .models import Category, User,Auction,Comment,Category,Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)

