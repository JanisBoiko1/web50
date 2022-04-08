import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post


def index(request):
    user_id = request.user.id
    return render(request, "network/index.html", {
        "userId": user_id,
    })
   
@login_required
def following_page(request):
    return render(request, "network/following.html")

@csrf_exempt
@login_required
def compose(request):
     # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get post data
    data = json.loads(request.body)

    # Get contents of post
    content = data.get("content", "")
    #print(content)

    # Create post

    post = Post(
        user=request.user,
        poster=request.user,
        content=content,
        likes= 0
     )
    print(post)
    post.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)

def showPosts(request, showGroup, user_id):

    # Filter posts
    if showGroup == "all":
        posts = Post.objects.all()
            
    elif showGroup == "following":
        #query db for all users
        users = User.objects.all()
        #put queryset on list
        list_of_users = list(users)
        #creat empty list posts
        posts = []
        
        #iterate the users
        for individual_user in list_of_users:
            #get who are their followers
            who_are_their_followers = individual_user.followers.all()
            
            #put followers in list
            list_of_who_are_their_followers = list(who_are_their_followers)
            print(list_of_who_are_their_followers)
            
            #get each follower from the list
            for follower2 in list_of_who_are_their_followers:
                print(follower2)
                
                #check if follower is the requesting user
                if(request.user.username == str(follower2)):
                    
                    #if so, get posts from the user our requesting user is following
                    copies = Post.objects.filter(poster=individual_user)
                    
                    #transform querysets in copies into a list, iterate this list and append each set into posts
                    if(copies):
                        print(copies)
                        for copy in list(copies):
                            posts.append(copy)
                            
        #then return list as json 
        print(posts)      
        return JsonResponse([post.serialize() for post in posts], safe=False)
       
            
    elif showGroup =="profile":
        posts = Post.objects.filter(user=user_id)
    
    else:
        return JsonResponse({"error": "Invalid adress."}, status=400)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

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
    
@csrf_exempt
# @login_required    
def profile(request, user_id):
    
    if request.method == "PUT":
        #when a profile is followed, the user followed gets the logged user id as their new follower 
        #https://stackoverflow.com/questions/15384665/django-manytomanyfield-add-user
        profile = User.objects.get(pk=user_id)
        
        data = json.loads(request.body)
        print(data.get("followers"))
        if(int(data.get("followers")) >= 0):
            user_following = User.objects.get(pk=data.get("followers"))
            profile.followers.add(user_following)
            profile.save()
            print(profile.followers.all())
            return HttpResponse(status=204)
        else:
            id = -(int(data.get("followers")))
            user_following = User.objects.get(pk=id)
            profile.followers.remove(user_following)
            profile.save()
            print(profile.followers.all())
            return HttpResponse(status=204)
        
    else:
        # Query for requested profile
        profile = User.objects.get(pk=user_id)
        followers = profile.followers
        print(profile.followers.all())
        # print(user_id)
        
        # define if user can or cannot follow this profile (if user's profile and 
        # requesting user are the same person, then thefollow button should be)
        buttons = True
        logged = 0
        if(request.user.id):
            logged = request.user.id
    
        if(request.user.id == user_id):
            buttons = False

        #get how many people user follows
        
        #creat following
        following = 0
        #query db for all users
        users = User.objects.all()
        #put queryset on list
        list_of_users = list(users)
        
        #iterate the users
        for individual_user in list_of_users:
            
            #get who are their followers
            who_are_their_followers = individual_user.followers.all()
            
            #put followers in list
            list_of_who_are_their_followers = list(who_are_their_followers)
            
            #get each follower from the list
            for follower2 in list_of_who_are_their_followers:

                #check if follower is the profile user, if so add 1 to following
                if(profile.username == str(follower2)):
                    following += 1
        
        #return all profile data
        return render(request, "network/profile.html", {
            "logged": logged,
            "userId" : user_id,
            "username": profile,
            "followers": followers.count(),
            "following": following,
            "buttons": buttons,
        
        })

@csrf_exempt
@login_required        
def individualPost(request, post_id):
    if request.method == "PUT":
        #get the post
        post = Post.objects.get(pk=post_id)
        #print(post)
        #get the api data
        data = json.loads(request.body)
        #print(data)
        
        #if data has content in it
        if data.get("content") is not None:
            post.content = data["content"]
        
        #print(post.content)
                    
        #if data had likes in it
        if data.get("likes") is not None:
            if(data.get("likes") == 1):
                post.likes +=1
            else:
                post.likes -=1
            
            # print(post.likes)
            # print(data.get("likes"))
        
        post.save()
        return HttpResponse(status=204)
        
