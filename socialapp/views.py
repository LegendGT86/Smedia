from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm

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
        messages.success(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home')
    
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
        messages.success(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home')