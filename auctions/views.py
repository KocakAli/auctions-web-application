import auctions
from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import *
from .models import Category, User
from django.contrib.auth.decorators import login_required


def index(request):
    cur_user = request.user
    auctions = Auction.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'auctions':auctions,
        'categories': categories
    })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        cur_user = request.user
        
        
        return render(request, 'auctions/add_list.html',{
            'categories': categories
        })
    else:
        cur_user = request.user
        title= request.POST['title'].capitalize()
        text= request.POST['text']
        cat = Category.objects.get(pk=int(request.POST['cat']))
        start_bid = request.POST['bid']
        print(cat)
        Auction.user = User.objects.get(pk =int(cur_user.id))
        auc_name = Auction.objects.filter(name=title,auction_user=cur_user)
        categories = Category.objects.all()
        if len(auc_name) !=0:
            message= 'You can not create the same list twice'
            return render(request,'auctions/add_list.html',{
            'message': message,
            'categories': categories
        })
        auc= Auction(name=f'{title}',text=f'{text}',auction_user=Auction.user,category=cat,image=request.POST['img'],bid = start_bid)
        auc.save()
        return HttpResponseRedirect(reverse('auction',args=(auc.id,)))

def auction(request, auction_id):
    auction = Auction.objects.get(pk = auction_id)
    print(auction_id)
    comments = Comment.objects.filter(comment_auction_id = auction_id)
    print(comments)
    return render(request,'auctions/auction.html',{
            'auction':auction,
            'comments':comments
            
            })

@login_required(login_url='/login')
def watch(request):
    if request.method == 'POST':
        auction_id = Auction.objects.get(pk=request.POST['auction_id'])
        watch = User.objects.get(username=request.POST.get('watch'))
        print(watch)
        username = User.objects.get(username = request.POST.get('username'))
        comments = Comment.objects.filter(comment_auction_id = auction_id)
        cur_username =request.user.username
        check = Watchlist.objects.filter(watch_id = watch, watch_auc_id =auction_id)
        if len(check) != 0:
            message = 'You have already this list on you watchlist'
            return render(request,'auctions/auction.html',{
                'message':message,
                'comments':comments,
                'auction':auction_id,
                'name':cur_username
            })
        save= Watchlist(watch=watch,watch_user= username, watch_auc = auction_id)
        save.save()
        watchlists = Watchlist.objects.filter(watch=watch)
        print(watchlists)
        return HttpResponseRedirect(reverse('show',kwargs={'name':cur_username}))



@login_required(login_url='/login')
def bid(request, auction_id):
    comments = Comment.objects.filter(comment_auction_id = auction_id)
    auction = Auction.objects.get(pk = auction_id)
    bid = int(request.POST['bid'])
    if bid < auction.bid :
        message = 'Your bid is lower than current price'
        return render(request,'auctions/auction.html',{
            'auction':auction,
            'message':message,
            'comments':comments
        })
    elif bid==auction.bid:
        message = 'Your bid can not be equal to current price'
        return render(request,'auctions/auction.html',{
            'auction':auction,
            'message':message,
            'comments':comments
        })

    cur_user = request.user
    if cur_user.id == auction.auction_user.id:
        message = 'You can not bid your own list'
        return render(request,'auctions/auction.html',{
            'message':message,
            'auction':auction,
            'comments':comments
        })
    auction.bid = bid
    auction.last_bid = User.objects.get(pk=cur_user.id)
    auction.save()
    return render(request,'auctions/auction.html',{
        'auction':auction,
        'user':cur_user,
        'comments':comments
    })

@login_required(login_url='/login')
def comment(request):
    cur_user = request.user
    User.username =User.objects.get(username= cur_user.username)
    Auction.id = Auction.objects.get(pk = request.POST['auction_id'])
    id = request.POST['auction_id']
    title = request.POST['title']
    comment = request.POST['comment']
    comment = Comment(title=title, comment=comment, comment_user=User.username, comment_auction=Auction.id)
    comment.save()
    return HttpResponseRedirect(reverse("auction",args=(id,)))


def close(request):
    if request.method =='POST':
        auction_id = Auction.objects.get(pk=request.POST['auction_id'])
        auction_id.closed = 1
        auction_id.save()
        return redirect('auction',auction_id = auction_id.id)


def show(request,name):
    user = User.objects.get(username=name)
    print(user)
    watchlists = Watchlist.objects.filter(watch=user)
    print(watchlists)
    return render(request, 'auctions/watchlist.html',{
        'watchlists':watchlists,
        'name':name
    })


def cat(request):
    if request.method == 'POST':
        cat_name = request.POST['cat']
        cat = Category.objects.get(pk=cat_name)
        auctions = Auction.objects.filter(category = cat.id)
        categories = Category.objects.all()
        if cat.id == 1:
            return HttpResponseRedirect(reverse('index'))
     

        return render(request, 'auctions/index.html',{
            'auctions':auctions,
            'categories':categories
        })

def remove(request,watch_id):
    list = Watchlist.objects.get(pk= watch_id)
    list.delete()
    return HttpResponseRedirect(reverse('index'))