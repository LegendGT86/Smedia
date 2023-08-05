from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Profile, Tweet

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all()
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
        return render(request, "profile.html",{"profile":profile})
    else:
        messages.success(request, ("Sorry but you must be logged in to view this page"))
        return redirect('home')