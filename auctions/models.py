from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField


class User(AbstractUser):
    def __str__(self):
        return f'{self.id}. User: {self.username} {self.email}'


class Category(models.Model):
    name= models.CharField(max_length=32)

class Auction(models.Model):
    name = models.CharField(max_length=32)
    text = models.CharField(max_length=256)
    auction_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auc_users')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='categories')
    image = models.CharField(max_length=256)
    bid = models.IntegerField(default=0)
    last_bid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auc_lastbid',null=True,)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"list name:{self.name} list text{self.text} created by:{self.auction_user}"

class Comment(models.Model):
    title=models.CharField(max_length=256)
    comment =models.CharField(max_length=256)
    comment_user =models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_comment')
    comment_auction = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name='auctions_comment')

class Watchlist(models.Model):
    watch= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_belong')
    watch_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_watch')
    watch_auc = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name='auctions_watch')
    
    def __str__(self):
        return f"{self.watch_user}'s {self.watch_auc}"
   