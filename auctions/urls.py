from auctions.models import Category
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list", views.list, name='list'),
    path("list/<int:auction_id>", views.auction, name='auction'),
    path("watchlist",views.watch, name='watchlist'),
    path('watchlist/<str:name>',views.show, name='show'),
    path("bid/<int:auction_id>", views.bid, name='bid'),
    path("comment",views.comment, name='comment'),
    path("close", views.close, name='close'),
    path("cat", views.cat,name='cat'),
    path('remove/<int:watch_id>', views.remove, name='remove')
]
