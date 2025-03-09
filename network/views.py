from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Follow, Like
from django.core.paginator import Paginator
from .models import User
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def edit(request, id):
    data = json.loads(request.body)
    edit_post = Post.objects.get(pk=id)
    edit_post.content = data["content"]
    edit_post.save()
    return JsonResponse({"message": "Change successful", "data": data["content"] })

@csrf_exempt
def remove_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    like_count = Like.objects.filter(post=post).count()  
    return JsonResponse({"message": "Like removed", "like_count": like_count, "isliked": False})

@csrf_exempt
def add_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    newlike = Like(user=user, post=post)
    newlike.save()
    like_count = Like.objects.filter(post=post).count()  
    return JsonResponse({"message": "Like added", "like_count": like_count, "isliked": True})

@csrf_exempt
def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(allPosts, 10)
    pageNumber = request.GET.get('page')
    posts_of_the_page = paginator.get_page(pageNumber)
    allLikes = Like.objects.all()
    whoYouLiked = []
    for post in posts_of_the_page:
        post.like_count = Like.objects.filter(post=post).count()   
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []
    return render(request, "network/index.html",{
        "posts": posts_of_the_page,
        "whoYouLiked": whoYouLiked
    })

@csrf_exempt
def profile(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    if user is None:
        return HttpResponse("User not found")
    else:
        following = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(user_followed=user)
        allPosts = Post.objects.filter(user=user).order_by("id").reverse()
        numberofposts = allPosts.count

        try:
            checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
            if len(checkFollow) != 0:
                isFollowing = True
            else:
                isFollowing = False
        except:
            isFollowing = False

        paginator = Paginator(allPosts, 10)
        page_number = request.GET.get('page')
        posts_of_the_page = paginator.get_page(page_number)
        allLikes = Like.objects.all()
        whoYouLiked = []
        for post in posts_of_the_page:
            post.like_count = Like.objects.filter(post=post).count()   

        try:
            for like in allLikes:
                if like.user.id == request.user.id:
                    whoYouLiked.append(like.post.id)
        except:
            whoYouLiked = []

        return render(request, 'network/profile.html', {
            "posts" : posts_of_the_page,
            "username": user.username,
            "following": following,
            "followers": followers,
            "isfollowing": isFollowing,
            "user_profile": user,
            "number": numberofposts,
            "whoYouLiked": whoYouLiked
        })

@csrf_exempt
def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    followingPeople = Follow.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by('id').reverse()
    followingPosts = []
    for post in allPosts:
        for person in followingPeople:
            if person.user_followed == post.user:
                followingPosts.append(post)

    paginator = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    allLikes = Like.objects.all()
    whoYouLiked = []
    for post in posts_of_the_page:
         post.like_count = Like.objects.filter(post=post).count()   

    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []
    return render(request, 'network/following.html', {
        'posts': posts_of_the_page,
        'whoYouLiked': whoYouLiked
    })    

@csrf_exempt
def follow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow(user=currentUser, user_followed = userfollowData)
    f.save()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


@csrf_exempt
def unfollow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=currentUser, user_followed = userfollowData)
    f.delete()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

@csrf_exempt
def newPost(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
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

@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
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
