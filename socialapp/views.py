from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# Create your views here.
#currently this enables user logged in to see all tweets but cannot tweet from account if not logged in
def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("Your thoughts have been shared"))
                return redirect('home')
            
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets, "form":form})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.warning(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home')

def unfollow(request,pk):
    if request.user.is_authenticated:
        #get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        #Unfollow the user
        request.user.profile.follows.remove(profile)
        #save our profile
        request.user.profile.save()
        #return message
        messages.warning(request, (f"You have successfully unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.warning(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home') 
    
def follow(request,pk):
    if request.user.is_authenticated:
        #get the profile to follow
        profile = Profile.objects.get(user_id=pk)
        #Unfollow the user
        request.user.profile.follows.add(profile)
        #save our profile
        request.user.profile.save()
        #return message
        messages.warning(request, (f"You have successfully followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.warning(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home') 
    #consider if request.user.id == pk: and objects.exclude(user_id = pk) to remove option to follow self


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        #POST form logic
        if request.method == "POST":
            #Get current user ID
            current_user_profile = request.user.profile
            #Get form data
            action= request.POST['follow']
            #Decide to follow or unfollow
            if action =="unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            #save the profile changes
            current_user_profile.save()    
        return render(request, "profile.html",{"profile":profile, "tweets" : tweets})
    else:
        messages.warning(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home')   

def followers (request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'followers.html', {"profiles":profiles})
        else:
            messages.warning(request, ("You cannot view others profile pages"))
            return redirect('home') 
    else:
        messages.warning(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home')    

def follows (request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'follows.html', {"profiles":profiles})
        else:
            messages.warning(request, ("You cannot view others profile pages"))
            return redirect('home') 
    else:
        messages.warning(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home')        

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, (f'Congrads, you have been successfully logged in {username}'))
            return redirect('home')
        
        else:
            messages.error(request, ("Username or Password is incorrect"))
            return redirect('login')
    else:
        return render(request, "login.html",{})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully signed out, bye for now"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            #Login User
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, (f'You have successfully registered, Welcome {first_name}'))
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, "register.html",{'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id = request.user.id)
        #Get forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance= current_user)
        profile_form = ProfilePicForm(request.POST or None ,request.FILES or None, instance= profile_user)

        if user_form.is_valid() and profile_form.is_valid():
           user_form.save()
           profile_form.save()

           login(request, current_user)
           messages.success(request, ("Your profile has been updated"))
           return redirect('home')
        
        return render(request, "update_user.html",{'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("You must be logged in to view that page"))
        return redirect('home')

def tweet_like(request,pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to view that page"))
        return redirect('home')
    
def tweet_show(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    if tweet:
        return render(request, "show_tweet.html",{'tweet':tweet})
    else:
        messages.success(request,("That tweet does not exist"))
        return redirect('home')
    
def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        #Check to see if user owns tweet
        if request.user.username == tweet.user.username:
            tweet.delete()
            messages.success(request, ("This tweet has been successfully Deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.warning(request, ("This is somebody elses tweet..."))
            return redirect('home')
    else:
        messages.success(request, ("Please Log In To Continue..."))
        return redirect(request.META.get("HTTP_REFERER"))
    
def edit_tweet(request, pk):
        if request.user.is_authenticated:
            #grab the tweet first
            tweet = get_object_or_404(Tweet, id=pk)
            if request.user.username == tweet.user.username:
                form = TweetForm(request.POST or None, instance= tweet)
                if request.method == "POST":
                    if form.is_valid():
                        tweet = form.save(commit=False)
                        tweet.user = request.user
                        tweet.save()
                        messages.success(request, ("Your tweet has been updated"))
                        return redirect('home')
                else:
                   return render(request, "edit_tweet.html",{'form':form, 'tweet':tweet})
            else:
                messages.warning(request, ("This is somebody elses tweet..."))
                return redirect('home')
        else:
            messages.success(request, ("Please Log In To Continue..."))
            return redirect('home')
        
def notes (request):
    return render(request, 'notes.html', {})
               
def search(request):
    if request.method =="POST":
        #grab input from form field
        search = request.POST['search']
        #search the database for the tweet
        searched = Tweet.objects.filter(body__contains = search)
        return render(request, 'search.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search.html', {})
    
def search_user(request):
    if request.method =="POST":
        #grab input from form field
        search = request.POST['search']
        #search the database for the tweet
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_user.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search_user.html', {})    