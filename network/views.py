import json

from network.forms import NewPostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post
from .forms import NewPostForm


def index(request):
    form = NewPostForm(request.POST)
    Posts = Post.objects.all()
    Posts = Posts.order_by("-time_created").all()
    paginator = Paginator(Posts, 10)

    page_number = request.GET.get('page')
    Posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "form": form,
        "Posts": Posts
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url = '/login')
def create_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        creator = request.user
        if form.is_valid():
            content = form.cleaned_data["Post_content"]
            
            new_post = Post(
                content = content,
                post_creator = creator
            )
            
            new_post.save()
            return redirect("index")

        else:
            return redirect("index")
    else:
        return redirect("index")

@login_required(login_url = '/login')
def get_profile(request,username):
    Posts = Post.objects.filter(post_creator__username = username).order_by('-time_created').all()
    profile_id = User.objects.filter(username = username).get().id
    active_user = request.user
    followers = User.objects.get(username = username).followers.all()
    if active_user in followers:
        btn_text = "Unfollow"
    else:
        btn_text = "Follow"
    if str(active_user) == str(username):
        is_user = 1
    else: 
        is_user = 0
    return render(request, "network/profile.html", {
        "username": username,
        "profile_id": profile_id,
        "Posts": Posts,
        "is_user": is_user,
        "followers": followers,
        "btn_text": btn_text,
        "active_user": active_user
    })

@login_required(login_url = '/login')
@csrf_exempt
def follow(request, username, action):
    if request.method == "POST":
        #content = json.loads(request.body)
        User1 = request.user #Current user (the one doing the following)
        User2 = User.objects.get(username = username) #The user being followed
        
        try:
            if action == "Follow":
                User1.following.add(User2)
                User1.save()

                User2.followers.add(User1)
                User2.save()

            if action == "Unfollow":
                User1.following.remove(User2)
                User1.save()

                User2.followers.remove(User1)
                User2.save()
            followers = User1.followers.count()+100#count the updated follower count
            return JsonResponse([followers],safe=False)
        except:
            return JsonResponse("Hi", status=400)
    else:
        redirect("") 

def followers(request, username):
    User_1 = User.objects.get(username = username)
    followers = User_1.followers.all()
    no_followers = User_1.followers.count()
    return render(request, "network/followers.html", {
                'no_followers': no_followers,
                "followers": followers
            })

@login_required
def following_posts(request):
    followed_users = list(User.objects.filter(followers = request.user).values_list('id', flat=True))
    followed_users_2 = list(User.objects.filter(followers = request.user).values_list('username', flat=True))
    Posts = Post.objects.filter(post_creator__in = followed_users)
    Posts = Posts.order_by("-time_created").all()

    paginator = Paginator(Posts, 10)

    page_number = request.GET.get('page')
    Posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "Posts": Posts,
        "following":followed_users,
        "followed_users_2": followed_users_2
    })

@csrf_exempt
@login_required
def like(request, post_id, status):
    if request.method == 'POST':
        post = Post.objects.get(id = post_id)
        user = User.objects.get(username = request.user)
        if status == "like":
            post.likes.add(user)
            return JsonResponse({"message": "Post liked successfully."}, status=201)
        elif status == "unlike":
            post.likes.remove(user)
            return JsonResponse({"message": "Post unliked successfully."}, status=201)
        else: 
            return JsonResponse({"error": "POST request required."}, status=400)