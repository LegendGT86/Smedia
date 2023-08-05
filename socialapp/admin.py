from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet

# unRegister your models here.
admin.site.unregister(Group)

#Embed profile into User on Django admin
class ProfileMerge(admin.StackedInline):
    model = Profile  
                        
#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username field on admin
    fields = ["username"]
    inlines = [ProfileMerge]

#Unregister innitial user
admin.site.unregister(User)

#Reregister user and profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

#Register tweets
admin.site.register(Tweet)